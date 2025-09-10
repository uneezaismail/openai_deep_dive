import asyncio
from typing import Any
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    input_guardrail,
    output_guardrail,
    InputGuardrailTripwireTriggered,
)
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)


# input guardrail
class BiologyCheck(BaseModel):
    is_biology: bool
    response: str

biology_checker = Agent(
    name="biology_checker",
    instructions="Check if the input is related to biology. Return is_biology=True/False.",
    model=model,
    output_type=BiologyCheck,
)

@input_guardrail()
async def biology_input_guardrail(ctx: RunContextWrapper, agent: Agent, input: str) -> GuardrailFunctionOutput:
    print(f"[Input Guardrail] Checking biology for: {agent.name} with input {input}")
    result = await Runner.run(biology_checker, input)
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=result.final_output.is_biology
    )


# output guardrail
class MathCheck(BaseModel):
    is_math: bool
    response: str

math_checker = Agent(
    name="math_checker",
    instructions="Check if the output is math related. Return is_math=True/False.",
    model=model,
    output_type=MathCheck,
)

@output_guardrail()
async def math_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: Any) -> GuardrailFunctionOutput:
    print(f"[Output Guardrail] Checking math for: {agent.name} with {output}")
    result = await Runner.run(math_checker, output)
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=result.final_output.is_math
    )


# handoff agent
customer_agent = Agent(
    name="customer_agent",
    instructions="You are a customer service agent. Answer politely and clearly.",
    model=model,
    output_guardrails=[math_output_guardrail],
)


# main agent
assistant = Agent(
    name="assistant",
    instructions="You are a helpful assistant. your task is to Handoff each query to customer_agent.",
    model=model,
    input_guardrails=[biology_input_guardrail], 
    handoffs=[customer_agent],              
)


async def main():
    try:
        
        result = await Runner.run(assistant, "What is 2 + 2?", max_turns=3)
        print("\nNO GUARDRAIL TRIGGERED\n")
        print("Final Output:\n", result.final_output)
        print("\nLast Agent:\n", result.last_agent)

    except InputGuardrailTripwireTriggered as e:
        print("Input Guardrail triggered (Biology detected)")
        print(e.guardrail_result.output)
        
    except OutputGuardrailTripwireTriggered as e:
        print("Output Guardrail triggered (Math detected)")
        print(e.guardrail_result.output)

asyncio.run(main())
