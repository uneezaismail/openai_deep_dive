from typing import Any
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    output_guardrail,
    set_tracing_disabled
)
from agents.run import RunConfig
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

config=RunConfig(
    model=model
) 


class BiologyOutput(BaseModel):
    is_biology: bool
    reasoning: str



guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the output is related to biology.",
    output_type=BiologyOutput,
    model=model
)

# function is required in outputGuardrail 
@output_guardrail(name="hello")
async def biology_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, agent_output: Any
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, agent_output,  run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_biology,
    )


agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with all type of their questions.",
    output_guardrails=[biology_guardrail],
    model=model
)

async def main():
    try:
        result = await Runner.run(agent, "what is 2 + 2?", run_config=config)
        print(result.final_output)
        print(result.last_agent)
        print("Guardrail didn't trip")


    except OutputGuardrailTripwireTriggered as e:
        print("guardrail tripped")
        print(e.guardrail_result.output)


asyncio.run(main())