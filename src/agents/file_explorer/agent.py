from src.framework.core.goals import Goal
from src.framework.core.agent import Agent
from src.framework.actions.registry import PythonActionRegistry
from src.framework.language.function_calling import AgentFunctionCallingActionLanguage
from src.framework.environment.environment import Environment
from src.framework.llm.client import generate_response
from . import actions  # This imports and registers all decorated functions


def create_file_explorer_agent() -> Agent:
    """Create and configure a file explorer agent"""

    goals = [
        Goal(
            priority=1,
            name="Gather Information",
            description="Read each file in the project to understand its structure and contents."
        ),
        Goal(
            priority=2,
            name="Generate Documentation",
            description="After reading all files, generate appropriate documentation based on the user's request."
        ),
        Goal(
            priority=3,
            name="Terminate",
            description="Call the terminate action when the task is complete, providing the final result in the message."
        )
    ]

    action_registry = PythonActionRegistry(tags=["file_operations", "system"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )


def create_readme_agent() -> Agent:
    """Create an agent specialized for README generation"""
    goals = [
        Goal(priority=1,
             name="Gather Information",
             description="Read each file in the project in order to build a deep understanding of the project in order to write a README"),
        Goal(priority=2,
             name="Terminate",
             description="Call terminate when done and provide a complete README for the project in the message parameter")
    ]

    action_registry = PythonActionRegistry(tags=["file_operations", "system"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )


def create_analysis_agent() -> Agent:
    """Create an agent specialized for code analysis"""
    goals = [
        Goal(priority=1,
             name="Code Analysis",
             description="Analyze the project structure and code files to understand the system architecture"),
        Goal(priority=2,
             name="Generate Analysis",
             description="Provide insights about code structure, potential improvements, and recommendations")
    ]

    action_registry = PythonActionRegistry(tags=["file_operations", "search", "system"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )