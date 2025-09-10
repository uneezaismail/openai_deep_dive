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


class Audiance(BaseModel):
    role:str


async def dynamic_instructions(ctx: RunContextWrapper, agent: Agent) -> str:
    role = ctx.context.role.lower()  
    print(f"\nThe context is : {role}\n")
    print(f"\nThe agent : {agent.name}\n")
    
    if role == "student":
        return "You are a marketing agent. Explain simply, step by step, with easy examples."
    
    elif role == "teacher":
        return "You are a marketing agent. Give clear, structured explanations with definitions."
    
    elif role == "developer":
        return "You are a marketing agent. Be technical, focus on practical use and efficiency."
    
    elif role == "business":
        return "You are a marketing agent. Highlight benefits, value, and real-world impact."
    
    else:
        return "You are a marketing agent. Explain clearly in a friendly, professional tone."

        
agent = Agent(  
    name="marketing_agent",
    instructions=dynamic_instructions,
    model=model,
)

async def main():
    
    result = await Runner.run(agent, "write a a short blog post on web development?", run_config=config, context=Audiance(role="Student"))
    print(result.final_output)

asyncio.run(main())


# NOTE:
# Context must always be the first parameter
# If you switch the order (agent first, ctx second), the SDK won’t be able to inject context properly and you’ll get a runtime error.
# this logic is written in output_schema.py Because inside output_schema.py, the SDK explicitly checks argument order

