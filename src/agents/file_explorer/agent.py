from src.framework.core.goals import Goal
from src.framework.core.agent import Agent
from src.framework.actions.registry import ActionRegistry
from src.framework.language.function_calling import AgentFunctionCallingActionLanguage
from src.framework.environment.environment import Environment
from src.framework.llm.client import generate_response
from .actions import create_file_explorer_actions

def create_file_explorer_agent() -> Agent:
    """Create and configure a file explorer agent"""
    
    # Define the agent's goals
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
    
    # Set up the action registry
    action_registry = ActionRegistry()
    for action in create_file_explorer_actions():
        action_registry.register(action)
    
    # Create the agent
    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )
    
    return agent