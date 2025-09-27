from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    RunContextWrapper,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.run import RunConfig
from pydantic import BaseModel
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



async def dynamic_instructions(ctx: RunContextWrapper, agent: Agent) -> str:
    return "You are a marketing agent. Explain simply, step by step, with easy examples."
        
agent = Agent(  
    name="marketing_agent",
    instructions=dynamic_instructions,
    model=model,
)

async def main():
    
    # direct access instructions
    get_instructions = agent.instructions
    print("\ndirect access instructions: \n",get_instructions)
    
    # get instruction through method
    get_system_prompt = await agent.get_system_prompt(run_context=None)
    print("\nget instruction through method: \n",get_system_prompt)
    
    
asyncio.run(main())



 # NOTE:
    # If we print(agent.instructions) directly here,
    # we will only see the FUNCTION REFERENCE (like <function dynamic_instructions at 0x...>)
    # because instructions is a callable.
    #
    # To actually EXECUTE the function and get the real text,
    # we must call agent.get_system_prompt().
    # This method checks:
    #   - if instructions is a string → returns it directly
    #   - if instructions is a function → runs it (await if async) and gets the text
    #
    # That’s why we use get_system_prompt(), not agent.instructions.