import os
import json
from litellm import completion
from ..core.prompt import Prompt

def generate_response(prompt: Prompt, model: str = "gpt-4o") -> str:
    """Call LLM to get response"""
    messages = prompt.messages
    tools = prompt.tools

    result = None

    if not tools:
        response = completion(
            model=model,
            messages=messages,
            max_tokens=1024
        )
        result = response.choices[0].message.content
    else:
        response = completion(
            model=model,
            messages=messages,
            tools=tools,
            max_tokens=1024
        )

        if response.choices[0].message.tool_calls:
            tool = response.choices[0].message.tool_calls[0]
            result = {
                "tool": tool.function.name,
                "args": json.loads(tool.function.arguments),
            }
            result = json.dumps(result)
        else:
            result = response.choices[0].message.content

    return result