import os
from typing import List
from src.framework.actions.action import Action

def read_project_file(name: str) -> str:
    with open(name, "r") as f:
        return f.read()

def list_project_files() -> List[str]:
    all_files = os.listdir(".")
    print(f"the list of project files in the listdir is {all_files}")
    return sorted([file for file in os.listdir(".") if file.endswith(".py")])

def create_file_explorer_actions():
    """Create and return file explorer specific actions"""
    actions = [
        Action(
            name="list_project_files",
            function=list_project_files,
            description="Lists all Python files in the project.",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            },
            terminal=False
        ),
        Action(
            name="read_project_file",
            function=read_project_file,
            description="Reads a file from the project.",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The name of the file to read"}
                },
                "required": ["name"]
            },
            terminal=False
        ),
        Action(
            name="terminate",
            function=lambda message: f"{message}\nTerminating...",
            description="Terminates the session and prints the message to the user.",
            parameters={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "The final message to display"}
                },
                "required": ["message"]
            },
            terminal=True
        )
    ]
    return actions