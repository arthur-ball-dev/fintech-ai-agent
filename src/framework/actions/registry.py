from typing import List, Optional
from .action import Action
from .decorators import tools

class ActionRegistry:
    def __init__(self):
        self.actions = {}

    def register(self, action: Action):
        self.actions[action.name] = action

    def get_action(self, name: str) -> Optional[Action]:
        return self.actions.get(name, None)

    def get_actions(self) -> List[Action]:
        """Get all registered actions"""
        return list(self.actions.values())


class PythonActionRegistry(ActionRegistry):
    def __init__(self, tags: List[str] = None, tool_names: List[str] = None):
        super().__init__()

        for tool_name, tool_desc in tools.items():

            if tool_names and tool_name not in tool_names:
                continue

            tool_tags = tool_desc.get("tags", [])
            if tags and not any(tag in tool_tags for tag in tags):
                continue

            # Register ALL matching tools (including terminate if it matches filters)
            self.register(Action(
                name=tool_name,
                function=tool_desc["function"],
                description=tool_desc["description"],
                parameters=tool_desc.get("parameters", {}),
                terminal=tool_desc.get("terminal", False)
            ))