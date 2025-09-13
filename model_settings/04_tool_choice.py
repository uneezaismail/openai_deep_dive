from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    ModelSettings,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool
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


# tool
@function_tool
def simple_tool(text: str) -> str:
    """
    A simple tool that echoes back the given text with a prefix.
    """
    return f"[TOOL EXECUTED] You entered: {text}"


#  Agent 1: tool_choice = "auto" 

# - Default mode.
# - The model decides whether or not to use a tool depending on the prompt.
# - If prompt matches a tool schema → tool will likely execute.
agent_auto = Agent(
    name="marketing_agent_auto",
    instructions="You are a professional marketing assistant. Explain concepts clearly and simply.",
    model=model,
    tools=[simple_tool],
    model_settings=ModelSettings(
        tool_choice="auto"
    )
)



#  Agent 2: tool_choice = "required" 

# - Tool will ALWAYS execute (even if irrelevant to prompt).
# - You can confirm this in traces.
agent_required = Agent(
    name="marketing_agent_required",
    instructions="You are a professional marketing assistant. Explain concepts clearly and simply.",
    model=model,
    tools=[simple_tool],
    model_settings=ModelSettings(
        tool_choice="required"
    )
)


#  Agent 3: tool_choice = "none" 

# - Tool will NEVER execute (even if the prompt clearly matches the tool).
# - Schema is still sent to LLM, but call is blocked.
agent_none = Agent(
    name="marketing_agent_none",
    instructions="You are a professional marketing assistant. Explain concepts clearly and simply.",
    model=model,
    tools=[simple_tool],
    model_settings=ModelSettings(
        tool_choice="none"
    )
)


# Agent 4: tool_choice="your_tool_name"

# - That specific tool will ALWAYS be called (forced).
# - Even if the prompt isn’t related at all.
agent_forced_tool = Agent(
    name="agent_forced_tool",
    instructions="You are a professional marketing assistant.",
    model=model,
    tools=[simple_tool],
    model_settings=ModelSettings(
        tool_choice="simple_tool"
        )
)

async def main():
    print("[bold green]--- Auto Tool Choice ---[/bold green]")
    result1 = await Runner.run(agent_auto, "Use the tool with input 'Hello World'", run_config=config)
    print(result1.final_output)

    print("\n[bold yellow]--- Required Tool Choice ---[/bold yellow]")
    result2 = await Runner.run(agent_required, "Just explain web development basics", run_config=config)
    print(result2.final_output)

    print("\n[bold red]--- None Tool Choice ---[/bold red]")
    result3 = await Runner.run(agent_none, "Use the tool with input 'Test this'", run_config=config)
    print(result3.final_output)

asyncio.run(main())



# NOTE on tool_choice:
# - "auto": LLM decides when to call a tool.
#
# - "required": Tool always executes (even if irrelevant).
#   → Important: In traces you may see the tool was invoked,
#     but the tool’s output might not always appear in the final_output.
#     (The agent can decide to summarize or omit it.)
#
# - "none": Tool never executes (even if prompt asks for tool).
#   → Important: Tool schema is still passed to the LLM,
#     but the call won’t happen.
#     If the final_output looks related to the tool, that’s because
#     the agent itself generated the answer — check traces for clarification.
