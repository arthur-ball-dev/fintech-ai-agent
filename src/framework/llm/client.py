import os
import json
from litellm import completion
from ..core.prompt import Prompt

# Verify API key is available
if not os.environ.get('OPENAI_API_KEY'):
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set it in your system environment variables."
    )


def generate_response(prompt: Prompt, model: str = "gpt-4o") -> str:
    """Call LLM to get response"""
    messages = prompt.messages
    tools = prompt.tools

    try:
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

            # Check the response model structure
            choice = response.choices[0]

            # Try to access tool_calls from the response model
            if hasattr(response, 'model_dump'):
                response_dict = response.model_dump()
                if 'choices' in response_dict and len(response_dict['choices']) > 0:
                    choice_data = response_dict['choices'][0]
                    if 'message' in choice_data and 'tool_calls' in choice_data['message'] and \
                            choice_data['message']['tool_calls']:
                        tool_call = choice_data['message']['tool_calls'][0]
                        result = {
                            "tool": tool_call['function']['name'],
                            "args": json.loads(tool_call['function']['arguments']),
                        }
                        result = json.dumps(result)
                    else:
                        # No tool calls, return content
                        result = choice_data['message'].get('content', '')
                else:
                    result = str(response)
            else:
                # Fallback to message content
                message = choice.message
                result = message.content if hasattr(message, 'content') and message.content else ""

    except Exception as e:
        print(f"ERROR in generate_response: {e}")
        import traceback
        traceback.print_exc()
        raise

    return result if result else ""