from dotenv import load_dotenv
import asyncio, os
from typing import Any, Optional
from agents import (
    Agent,
    ModelResponse,
    RunConfig,
    RunHooks,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    TResponseInputItem,
    set_tracing_disabled,
    function_tool,
    enable_verbose_stdout_logging,
    RunContextWrapper,
    Tool,
)
from rich import print

load_dotenv()
# enable_verbose_stdout_logging()

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

config = RunConfig(
    model=model
)


@function_tool
def word_count(text: str) -> str:
    """Count the number of words in the given text."""
    count = len(text.split())
    return f"The text contains {count} words."



class MyRunHooks(RunHooks):
    """Global hooks for the entire run (all agents, tools, and handoffs)."""

    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        print(f"[RunHook] Agent started: {agent.name}")

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        print(f"[RunHook] Agent ended: {agent.name}, output: {output}")

    async def on_llm_start(
        self,
        context: RunContextWrapper,
        agent: Agent,
        system_prompt: Optional[str],
        input_items: list[TResponseInputItem],
    ) -> None:
        print(f"[RunHook] LLM start for {agent.name}")

    async def on_llm_end(
        self,
        context: RunContextWrapper,
        agent: Agent,
        response: ModelResponse,
    ) -> None:
        print(f"[RunHook] LLM end for {agent.name}")

    async def on_handoff(
        self,
        context: RunContextWrapper,
        from_agent: Agent,
        to_agent: Agent,
    ) -> None:
        print(f"[RunHook] Handoff from {from_agent.name} to {to_agent.name}")

    async def on_tool_start(
        self,
        context: RunContextWrapper,
        agent: Agent,
        tool: Tool,
    ) -> None:
        print(f"[RunHook] Tool started: {tool.name} (Agent: {agent.name})")

    async def on_tool_end(
        self,
        context: RunContextWrapper,
        agent: Agent,
        tool: Tool,
        result: str,
    ) -> None:
        print(f"[RunHook] Tool ended: {tool.name}, result: {result}")



helper_agent = Agent(
    name="helper_agent",
    instructions="You are a helper agent that explains briefly and uses tools when needed.",
    model=model,
    tools=[word_count],
)



async def main():
    result = await Runner.run(
        helper_agent,
        "Please explain what HTML and CSS are, then count the words.",
        run_config=config,
        hooks=MyRunHooks()  
    )
    print("\nFinal Output:\n", result.final_output)


asyncio.run(main())
