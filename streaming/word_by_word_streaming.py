
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
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")


async def main():
    
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
        name="Joker",
        instructions="You are a helpful assistant.",
        model=model
    )

    # Run streamed
    result = Runner.run_streamed(agent, input="Please tell me 50 jokes.")

    # Process token-by-token / word-by-word manually
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            text_chunk = event.data.delta

            for char in text_chunk:  # letter by letter
                print(char, end="", flush=True)
                await asyncio.sleep(0.0001)


asyncio.run(main())

