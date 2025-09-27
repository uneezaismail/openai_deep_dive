from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.run import RunConfig
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

config=RunConfig(
    model=model
) 

agent = Agent(  
    name="marketing_agent",
    instructions="You are a professional marketing assistant. Explain concepts clearly and simply.",
    model=model,
)

async def main():
    
    result = await Runner.run(agent, "write a a short blog post for students on web development?", run_config=config)
    print(result.final_output)

asyncio.run(main())






# from dotenv import load_dotenv
# import asyncio, os
# from agents import (
#     Agent,
#     Runner,
#     AsyncOpenAI,
#     OpenAIChatCompletionsModel,
#     function_tool,
#     set_tracing_disabled
# )
# from agents.run import RunConfig
# from rich import print

# load_dotenv()
# # set_tracing_disabled(disabled=True)

# API_KEY=os.environ.get("GEMINI_API_KEY")
# OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

# model=OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=AsyncOpenAI(
#         api_key=API_KEY,
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
#     )
# )

# config=RunConfig(
#     model=model
# ) 

# agent = Agent(  
#     name="marketing_agent",
#     instructions="You are a professional marketing assistant. Explain concepts clearly and simply.",
#     model=model,
# )

# @function_tool
# def get_user(user:str):
#     return f"{user} is a girl"

# main_agent = Agent(  
#     name="main_agent",
#     instructions="You are a helper agent.you do not do any thing just first use tools and then handoff",
#     model=model,
#     handoffs=[agent],
#     tools=[get_user]
# )

# async def main():
    
#     result = await Runner.run(main_agent, "give me uneeza data and write a a short blog post for students on web development?", run_config=config)
#     print(result.final_output)
#     print(result.last_agent)

# asyncio.run(main())

