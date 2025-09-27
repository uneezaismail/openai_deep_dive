from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    FunctionTool,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    function_tool,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.run import RunConfig
from rich import print

load_dotenv()
# set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

@function_tool
def get_date():
    return "date"

@function_tool
def get_user():
    return "user"

agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    model=model,
    tools=[get_date,get_user]
)


async def main():
    
    all_tools = await agent.get_all_tools(run_context=None)
    print(all_tools)


asyncio.run(main())
