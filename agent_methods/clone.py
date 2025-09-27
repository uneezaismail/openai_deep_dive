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

model = OpenAIChatCompletionsModel(
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

@function_tool
def get_weather():
    return "weather"

@function_tool
def get_time():
    return "time"


main_agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    model=model,
    tools=[get_date]
)

cloned_agent = main_agent.clone()

# Both share same reference of tools list at this point
main_agent.tools.append(get_user)      # adds to BOTH
cloned_agent.tools.append(get_weather) # also affects BOTH


async def main():
    main_agent_all_tools = await main_agent.get_all_tools(run_context=None)
    print(f"main_agent_all_tools \n", main_agent_all_tools)
    
    cloned_agent_all_tools = await cloned_agent.get_all_tools(run_context=None)
    print(f"\ncloned_agent_all_tools\n", cloned_agent_all_tools)
    
    # Reassign tools -> new list in memory (breaks the shared link)
    cloned_agent.tools = [get_time]
    cloned_agent_all_tools_after = await cloned_agent.get_all_tools(run_context=None)
    print(f"\ncloned_agent_all_tools after reassigning\n", cloned_agent_all_tools_after)
    
    main_agent_all_tools = await main_agent.get_all_tools(run_context=None)
    print(f"main_agent_all_tools after reassigning tools to cloned agent\n", main_agent_all_tools)


asyncio.run(main())


# 1. tools and handoffs are mutable lists.
#    When we clone the agent, Python just copies the REFERENCE,
#    so both agents point to the same list in memory.

# 2. Because of this, if we do:
#       cloned_agent.tools.append(weather)
#    it will ALSO appear in main_agent.tools (they share the list).

# 3. But if we REASSIGN like this:
#       cloned_agent.tools = [time]
#    then Python creates a NEW list in memory just for cloned_agent.
#    From that point, main_agent.tools and cloned_agent.tools are different.

# 4. Why does this happen?
#    - Lists are mutable (can be changed after creation).
#    - When two variables point to the same list, any change is seen by both.
#    - Reassigning with "=" breaks the shared link and gives a fresh list,
#      so changes won’t affect the other anymore.
