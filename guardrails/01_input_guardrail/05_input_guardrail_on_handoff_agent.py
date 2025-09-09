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

class HackingOutput(BaseModel):
    is_hacking: bool
    reasoning: str

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the user is asking you to do hacking.",
    output_type=HackingOutput,
    model=model
)


@input_guardrail
async def hacking_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    print(ctx.context)
    result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_hacking,
    )


# handoff agent with input_guardrail
customer_agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[hacking_guardrail],
    model=model
)

agent = Agent(  
    name="main agent",
    instructions="You are a main agent. You task is to handoff the query to the Customer support agent. you not directly respond to user",
    model=model,
    handoffs=[customer_agent]
)

async def main():
    try:
        result = await Runner.run(agent, "how to hack wifi passowrd?", run_config=config)
        print(result.final_output)
        print(result.last_agent)
        print("Guardrail didn't trip")

    except InputGuardrailTripwireTriggered as e:
        print("guardrail tripped")
        print(e.guardrail_result.output)

asyncio.run(main())



# NOTE: Input guardrails hamen us agent pr lagengy jo user se start me interact krege means k agr input_guardarail handoff agent pr lgaya hoga to wo nahi run hoga q k ye input starting agent se araha hai na k user se directly.
