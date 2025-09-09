from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrail,
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

async def input_guadrail(ctx, agent, input):
    # guardrail agent ko run karwao
    result = await Runner.run(
        guardrail_agent,
        input,
        context=ctx.context,
        run_config=config
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,  # yeh HackingOutput hoga
        tripwire_triggered=result.final_output.is_hacking,
    )



my_input_guardrail=InputGuardrail(
    name="input_guadrails",
    guardrail_function=input_guadrail,
)



agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[my_input_guardrail],
    model=model
)


async def main():
    try:
        result = await Runner.run(agent, "how to 2 + 2?", run_config=config)
        print(result.final_output)
        print(result.last_agent)
        print("Guardrail didn't trip")

    except InputGuardrailTripwireTriggered as e:
        print("guardrail tripped")
        print(e.guardrail_result.output)



if __name__ == "__main__":
    asyncio.run(main())
    
    