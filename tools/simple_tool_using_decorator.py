from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    ModelSettings,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled,
    enable_verbose_stdout_logging
)
from agents.run import RunConfig
from rich import print

load_dotenv()

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

@function_tool
def get_user_data(name:str):
    return f"{name} is user."

agent = Agent(  
    name="helper_agent",
    instructions="You are a helper agent.must use tool to get user data and do not give answer from your own",
    model=model,
    tools=[get_user_data],
)


async def main():
    
    result = await Runner.run(agent, "give user uneeza data.")
    print(result.final_output)

asyncio.run(main())

