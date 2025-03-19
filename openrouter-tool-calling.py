import json, requests
from openai import OpenAI
import os

import tools
from tools import search_gutenberg_books
from tool2schema import FindToolEnabledSchemas, SchemaType

TOOL_MAPPING = {"search_gutenberg_books": search_gutenberg_books}


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "anthropic/claude-3.5-sonnet:beta"
openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

task = "What are the titles of some James Joyce books?"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {
        "role": "user",
        "content": task,
    },
]


request1 = {
    "model": MODEL,
    "tools": FindToolEnabledSchemas(tools, SchemaType.OPENAI_API),
    "messages": messages,
}
response1 = openai_client.chat.completions.create(**request1)
if response1.choices[0].finish_reason == "tool_calls":
    tool_calls = response1.choices[0].message.tool_calls
    print("tool_calls:\n")
    print(tool_calls)


# append tool calls and result of tool calls to messages
messages.append(response1.choices[0].message)
for tool_call in tool_calls:
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)
    tool_response = TOOL_MAPPING[tool_name](**tool_args)
    messages.append(
        {
            "role": "tool",  # NOTE: role can be tool
            "tool_call_id": tool_call.id,
            "name": tool_name,
            "content": json.dumps(tool_response),
        }
    )
request2 = {"model": MODEL, "messages": messages}

response2 = openai_client.chat.completions.create(**request2)
print(response2.choices[0].message.content)
