from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    output_guardrail,
    set_tracing_disabled,
    enable_verbose_stdout_logging
)
from agents.run import RunConfig
from rich import print

load_dotenv()
# set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()

API_KEY=os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)



class HackingOutput(BaseModel):
    is_hacking: bool
    reasoning: str

guardrail_agent = Agent( 
    name="agent Guardrail check",
    instructions="Check if the user is asking you to do hacking.",
    model=model,
    output_type=HackingOutput
)

# function is required in InputGuardrail 
@input_guardrail
async def hacking_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    print("hello from Agent Guardrail")
    result = await Runner.run(guardrail_agent, input)
    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_hacking,
    )

    
class BiologyOutput(BaseModel):
    is_biology: bool
    reasoning: str



biology_guardrail_agent = Agent( 
    name="Runner Guardrail check",
    instructions="Check if the output is related to biology.",
    model=model,
    output_type=BiologyOutput
)

@input_guardrail
async def biology_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    print("hi from Runner Guardrail")
    result = await Runner.run(biology_guardrail_agent, input)
    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_biology,
    )

config=RunConfig(
    model=model,
    input_guardrails=[hacking_guardrail],
)

agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    model=model,
    input_guardrails=[biology_guardrail]
)

async def main():
    try:
        result = await Runner.run(agent, "what is cell? and how to hack wifi passowrd? ", run_config=config)
        print(result.final_output)
        # print(result.last_agent)
        print("Guardrail didn't trip")

    except InputGuardrailTripwireTriggered as e:
        print("guardrail tripped")
        # print(e.guardrail_result.output)


asyncio.run(main())