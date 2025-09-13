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

# Low randomness → very focused, predictable, usually the same response every time
agent = Agent(  
    name="marketing_agent",
    instructions="You are a professional marketing assistant. Explain concepts clearly and simply.",
    model=model,
    model_settings=ModelSettings(
        temperature=0.2  
    )
)

# Medium randomness → balanced, creative but still reliable
agent = Agent(  
    name="marketing_agent",
    instructions="You are a professional marketing assistant. Explain concepts clearly and simply.",
    model=model,
    model_settings=ModelSettings(
        temperature=0.7  
    )
)

# High randomness → very creative, unpredictable (Not Safe)
agent = Agent(  
    name="marketing_agent",
    instructions="You are a professional marketing assistant. Explain concepts clearly and simply.",
    model=model,
    model_settings=ModelSettings(
        temperature=2.0  
    )
)

async def main():
    result = await Runner.run(agent, "write a short blog post for students on web development?", run_config=config)
    print(result.final_output)

asyncio.run(main())



# NOTE: You might still get the same response on different temperatures.
# This is because even at high temperature, the model can choose earlier (common) words again.
