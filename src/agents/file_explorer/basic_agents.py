"""
Basic Utility Agents for File Operations and Documentation

These agents provide fundamental file exploration, documentation generation,
and code analysis capabilities with FinTech pattern awareness.
"""
from src.framework.core.goals import Goal
from src.framework.core.agent import Agent
from src.framework.actions.registry import PythonActionRegistry
from src.framework.language.function_calling import AgentFunctionCallingActionLanguage
from src.framework.environment.environment import Environment
from src.framework.llm.client import generate_response
from . import actions  # This imports and registers all decorated functions

def create_file_explorer_agent() -> Agent:
    """
    Create and configure a file explorer agent with FinTech awareness.
    Includes basic file operations plus financial pattern recognition.
    """
    goals = [
        Goal(
            priority=1,
            name="Gather Information",
            description="Read each file in the project to understand its structure and contents, paying attention to financial patterns and business logic."
        ),
        Goal(
            priority=2,
            name="Generate Documentation",
            description="After reading all files, generate appropriate documentation based on the user's request, highlighting any relevant financial technology patterns."
        ),
        Goal(
            priority=3,
            name="Terminate",
            description="Call the terminate action when the task is complete, providing the final result in the message."
        )
    ]

    # Include basic file operations plus FinTech analysis capabilities
    action_registry = PythonActionRegistry(tags=["file_operations", "system", "fintech"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )

def create_readme_agent() -> Agent:
    """
    Create an agent specialized for README generation with FinTech focus.
    Produces professional documentation highlighting financial technology capabilities.
    """
    goals = [
        Goal(
            priority=1,
            name="Comprehensive Project Analysis",
            description="Analyze the entire project including financial patterns, performance optimizations, and enterprise-grade features to create a comprehensive understanding."
        ),
        Goal(
            priority=2,
            name="Professional Documentation",
            description="Generate a professional README that highlights the project's capabilities, technical architecture, and any financial technology applications."
        ),
        Goal(
            priority=3,
            name="Terminate",
            description="Call terminate when done and provide a complete, professional README in the message parameter."
        )
    ]

    action_registry = PythonActionRegistry(tags=["file_operations", "system", "fintech", "analysis"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )

def create_code_analysis_agent() -> Agent:
    """
    Create an agent specialized for code analysis with FinTech insights.
    Provides architectural understanding and technical recommendations.
    """
    goals = [
        Goal(
            priority=1,
            name="Comprehensive Code Analysis",
            description="Analyze the project structure, code files, and architecture to understand the system from both technical and business perspectives."
        ),
        Goal(
            priority=2,
            name="Generate Technical Analysis",
            description="Provide detailed insights about code structure, architectural patterns, performance considerations, and strategic recommendations."
        ),
        Goal(
            priority=3,
            name="Terminate",
            description="Provide a comprehensive analysis report suitable for technical review."
        )
    ]

    action_registry = PythonActionRegistry(tags=["file_operations", "search", "system", "fintech", "analysis"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )