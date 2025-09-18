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

run_config = RunConfig(
    model=model,
    model_settings=ModelSettings(
        tool_choice="required",
        temperature=1.5,
        top_p=0.5
    )
) 

# tool
@function_tool
def simple_tool(text: str) -> str:
    """
    A simple tool that echoes back the given text with a prefix.
    """
    return f"[TOOL EXECUTED] You entered: {text}"


agent = Agent(
    name="marketing_agent_none",
    instructions="You are a helpful agent.Use Tool to answer queries.",
    model=model,
    tools=[simple_tool],
    model_settings=ModelSettings(
        tool_choice="none",
        max_tokens=1000
    )
)

model_settings = agent.model_settings.resolve(run_config.model_settings)

print("Agent settings:\n", agent.model_settings)
print("RunConfig settings:\n", run_config.model_settings)
print("Resolved settings:\n", model_settings)

async def main():
    print("[bold green]--- Agent With Both ModelSettings ---[/bold green]")
    result1 = await Runner.run(agent, "Use the tool with input 'Hello World'", run_config=run_config)
    print(result1.final_output)



asyncio.run(main())



# Agent.model_settings = Agent ke model settings. Agar na do, to sab None.

# RunConfig.model_settings = Runtime pe jo override karna ho. Agar na do, to sab None.

# resolve() → Dono ko merge karta hai.

# Agar dono me value hai → RunConfig wali le lega.

# Agar sirf Agent me hai → wahi use hogi.

# Agar dono None hain → model apne defaults use karega.

# Backend ma ye code likha ha run.py me agr aap bhi use krna chahty hn to custom Runner banana hoga