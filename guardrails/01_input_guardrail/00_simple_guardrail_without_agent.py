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

# function is required in InputGuardrail 
@input_guardrail
async def hacking_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    
    return GuardrailFunctionOutput(
        output_info=None, 
        tripwire_triggered=False,
    )


agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[hacking_guardrail],
    model=model
)

async def main():
    # try:
        result = await Runner.run(agent, "how to hack wifi passowrd?", run_config=config)
        print(result.final_output)
        print(result.last_agent)
        print("Guardrail didn't trip")

    # except InputGuardrailTripwireTriggered as e:
    #     print("guardrail tripped")
    #     print(e.guardrail_result.output)

asyncio.run(main())