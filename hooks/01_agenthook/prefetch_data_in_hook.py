from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio, os
from typing import Any, Optional
from agents import (
    Agent,
    AgentHooks,
    ModelResponse,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    TResponseInputItem,
    set_tracing_disabled,
    function_tool,
    enable_verbose_stdout_logging,
    RunContextWrapper,
    Tool
)
from agents.run import RunConfig
from rich import print

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

config = RunConfig(
    model=model
)


@dataclass
class UserInfo:
    name: Optional[str] = None  



class PreFetchHook(AgentHooks[UserInfo]):
    async def on_start(self, context: RunContextWrapper[UserInfo], agent: Agent):
        print(f"[Hook] on_start called, current name: {context.context.name}")
        context.context.name = "Ali"
        print(f"[Hook] Updated name to: {context.context.name}")


@function_tool
async def get_user_name(wrapper: RunContextWrapper[UserInfo]) -> str:
    return f"The user's name is {wrapper.context.name}"



agent = Agent[UserInfo](
    name="helper_agent",
    instructions="you are a helper agent .help user to get their data using tool",
    model=model,
    hooks=PreFetchHook(),
    tools=[get_user_name]
)



async def main():

    user_info = UserInfo()

    result = await Runner.run(
        starting_agent=agent,
        input="Could you please tell me user name",
        context=user_info,
    )
    print("\nFinal Output:", result.final_output)


asyncio.run(main())
