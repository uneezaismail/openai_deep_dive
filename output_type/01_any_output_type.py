from typing import Dict
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    AgentOutputSchema,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.run import RunConfig
from rich import print

load_dotenv()

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

agent = Agent(  
    name="developer agent",
    instructions="You are a developer agent. You help users with development questions.",
    model=model,
    output_type=list[str] # agent will give a list of str in output
)

async def main():
    
    result = await Runner.run(agent, "what is HTML and CSS?", run_config=config)
    print(result.final_output)

asyncio.run(main())



# agent always return plain-text (str) by-default
# by default the value of output_type is None
# we can customize it by using output_type

# output-type could be "Any" type or a "pydantic class or dataclass" or a custom type like AgentOutputSchemaBase or AgentOutputSchema 




# some basic output_types:

# output_type=bool 
# output_type=int
# output_type=list[str]




# for dict you need to disable strict schema for that you have to use AgentOutputSchema and a class
# class DevOutput(BaseModel):
#     html: str
#     css: str
    
# AgentOutputSchema(DevOutput, strict_json_schema=False)  