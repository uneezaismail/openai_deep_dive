from typing import Any
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    enable_verbose_stdout_logging
    
)
    
from agents.run import RunConfig,ModelInputData,CallModelData
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()

API_KEY=os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

# This function runs right before the model is called
def call_model_input_filterr(cm: CallModelData[Any]) -> ModelInputData:
    md = cm.model_data
    base = md.instructions or ""
    extra = f" Please prioritize concise answers and give 3 bullet points."
    new_instructions = base + extra
    new_input_list = list(md.input)
    return ModelInputData(input=new_input_list, instructions=new_instructions)


config=RunConfig(
    model=model,
    call_model_input_filter=call_model_input_filterr
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


# Explanantion
# call_model_input_filter:
# - This function lets you change the model’s input *just before* it runs.
# - It takes "CallModelData" (which includes the agent, context, and model input).
# - It must return "ModelInputData" (instructions + input).

# In this example:
# - We added extra instructions: "concise + 3 bullet points".
# - We returned a new ModelInputData with these updated instructions.

# What can we do here?
# Add or change instructions
# Modify the user’s input (filter, format, etc.)
# Inject extra context (metadata, style, etc.)