import json
from typing import List, Dict, Any
from .base import AgentLanguage
from ..core.prompt import Prompt
from ..core.goals import Goal
from ..actions.action import Action
from ..memory.memory import Memory
from ..environment.environment import Environment

class AgentFunctionCallingActionLanguage(AgentLanguage):
    def __init__(self):
        super().__init__()

    def format_goals(self, goals: List[Goal]) -> List[Dict]:
        sep = "\n-------------------\n"
        goal_instructions = "\n\n".join([f"{goal.name}:{sep}{goal.description}{sep}" for goal in goals])
        return [
            {"role": "system", "content": goal_instructions}
        ]

    def format_memory(self, memory: Memory) -> List[Dict]:
        items = memory.get_memories()
        mapped_items = []
        for item in items:
            content = item.get("content", None)
            if not content:
                content = json.dumps(item, indent=4)

            if item["type"] == "assistant":
                mapped_items.append({"role": "assistant", "content": content})
            elif item["type"] == "environment":
                mapped_items.append({"role": "assistant", "content": content})
            else:
                mapped_items.append({"role": "user", "content": content})

        return mapped_items

    def format_actions(self, actions: List[Action]) -> List[Dict]:
        tools = [
            {
                "type": "function",
                "function": {
                    "name": action.name,
                    "description": action.description[:1024],
                    "parameters": action.parameters,
                },
            } for action in actions
        ]
        return tools

    def construct_prompt(self,
                         actions: List[Action],
                         environment: Environment,
                         goals: List[Goal],
                         memory: Memory) -> Prompt:
        prompt = []
        prompt += self.format_goals(goals)
        prompt += self.format_memory(memory)
        tools = self.format_actions(actions)
        return Prompt(messages=prompt, tools=tools)

    def parse_response(self, response: str) -> dict:
        try:
            return json.loads(response)
        except Exception as e:
            return {
                "tool": "terminate",
                "args": {"message": response}
            }