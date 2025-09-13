from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    ModelSettings,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.run import RunConfig
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

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

# Agent 1: With frequency_penalty 

# frequency_penalty = 0.8
#   - Discourages repeating the same words/phrases.
#   - Useful for avoiding redundancy.
agent_frequency = Agent(  
    name="marketing_agent_frequency",
    instructions="You are a professional marketing assistant. Explain concepts clearly and simply.",
    model=model,
    model_settings=ModelSettings(
        frequency_penalty=0.8
    )
)



# Agent 2: With presence_penalty 

# presence_penalty = 0.8
#   - Encourages introducing new ideas/topics instead of circling around the same ones.
#   - Useful when you want variety in themes.
agent_presence = Agent(  
    name="marketing_agent_presence",
    instructions="You are a professional marketing assistant. Explain concepts clearly and simply.",
    model=model,
    model_settings=ModelSettings(
        presence_penalty=0.8
    )
)

async def main():
    print("\nFrequency Penalty Example\n\n")
    result1 = await Runner.run(agent_frequency, "write a short blog post for students on web development?", run_config=config)
    print(result1.final_output)

    print("\nPresence Penalty Example\n\n")
    result2 = await Runner.run(agent_presence, "write a short blog post for students on web development?", run_config=config)
    print(result2.final_output)

asyncio.run(main())


# NOTE:
# - `frequency_penalty` reduces repeating the same words.
# - `presence_penalty` pushes the model to bring in new topics/ideas.

