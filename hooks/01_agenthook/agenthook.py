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
# set_tracing_disabled(disabled=True)
# enable_verbose_stdout_logging()

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

# tool
@function_tool
def word_count(text: str) -> str:
    """Count the number of words in the given text."""
    count = len(text.split())
    return f"The text contains {count} words."


# hooks
class AgentEventHook(AgentHooks):
    # Runs when the agent starts
    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        print("Agent started hook")
        print(context.usage.input_tokens)

    # Runs when the agent finishes and gives output
    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        print("Agent ended hook")
        print(context.usage.output_tokens)

    # Runs just before the agent makes a request to the LLM
    async def on_llm_start(
        self,
        context: RunContextWrapper,
        agent: Agent,
        system_prompt: Optional[str],
        input_items: list[TResponseInputItem],
    ) -> None:
        print("LLM start hook")

    # Runs right after the LLM gives its response
    async def on_llm_end(
        self,
        context: RunContextWrapper,
        agent: Agent,
        response: ModelResponse,
    ) -> None:
        print("LLM end hook")

    # Runs when one agent hands off to another
    async def on_handoff(
        self,
        context: RunContextWrapper,
        agent: Agent,
        source: Agent,
    ) -> None:
        print(f"Handoff from {source.name} to {agent.name}")

    # Runs before a tool is called
    async def on_tool_start(
        self,
        context: RunContextWrapper,
        agent: Agent,
        tool: Tool,
    ) -> None:
        print(f"Tool started: {tool.name}")

    # Runs after a tool is done running
    async def on_tool_end(
        self,
        context: RunContextWrapper,
        agent: Agent,
        tool: Tool,
        result: str,
    ) -> None:
        print(f"Tool ended: {tool.name}, result: {result}")



review_agent = Agent(
    name="review_agent",
    instructions="You are a reviewer agent. Review and refine the output given by the helper agent.",
    model=model,
)


helper_agent = Agent(
    name="helper_agent",
    instructions="You are a helper agent that explains briefly and uses tools when needed.",
    model=model,
    tools=[word_count],   
    hooks=AgentEventHook(),
    handoffs= [review_agent]
)


async def main():
    result = await Runner.run(
        helper_agent,
        "Please explain what HTML and CSS are, then count the words.",
        run_config=config,
    )
    print("\nFinal Output:\n", result.final_output)


asyncio.run(main())
