from dataclasses import dataclass
import json
from typing import Any, Dict
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    AgentOutputSchema,
    AgentOutputSchemaBase,
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



# A custom schema example.
# Normally we just pass a dataclass or Pydantic model as output_type,
# but sometimes we need full control over the JSON schema and validation.
class CustomOutputSchema(AgentOutputSchemaBase):
    """Custom schema for developer agent."""

    def is_plain_text(self) -> bool:
        return False

    def name(self) -> str:
        return "CustomOutputSchema"

    def json_schema(self) -> dict[str, Any]:
        return {
             "type": "object",
        "properties": {
            "responses": {
                "type": "object",
                "properties": {     
                    "example": {"type": "string"}
                },
                "additionalProperties": {"type": "string"}
            }
        },
        "required": ["responses"]
    }

    def is_strict_json_schema(self) -> bool:
        return False  

    def validate_json(self, json_str: str) -> Any:
        json_obj = json.loads(json_str)
        return json_obj["responses"] 
 
    

agent = Agent(  
    name="developer agent",
    instructions="You are a developer agent. You help users with development questions.",
    model=model,
    output_type=CustomOutputSchema(),
)

async def main():
    
    result = await Runner.run(agent, "what is HTML and CSS?", run_config=config)
    print(result.final_output)

asyncio.run(main())



# Note:
# Most of the time you won’t need a custom output schema like this.
# It’s only useful when:
#   - your schema isn’t strictly compatible,
#   - or you want full control over how validation works.