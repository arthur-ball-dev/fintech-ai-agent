"""
Test script for the enhanced file explorer agent system.
Demonstrates decorator-based tools, specialized agents, and LLM-agnostic design.

This file tests the integration of Multiple Framework Components:
Decorators → Global Registry
Registry → Tag Filtering → Agent Creation
Agent → LLM Client → Multiple Providers

"""

from src.framework.core.agent import Agent
from src.framework.core.goals import Goal
from src.framework.core.prompt import Prompt
from src.framework.actions.registry import PythonActionRegistry
from src.framework.language.function_calling import AgentFunctionCallingActionLanguage
from src.framework.environment.environment import Environment
from src.framework.llm.client import generate_response
from src.agents.file_explorer.actions import *  # Import the decorated tools (Keep this line because it registers them automatically)


def test_tool_discovery():
    """Test that decorated tools are being discovered properly."""
    print("=== Tool Discovery Test ===")

    from src.framework.actions.decorators import tools, tools_by_tag

    print(f"Total registered tools: {len(tools)}")
    print(f"Available tools: {list(tools.keys())}")
    print(f"Available tags: {list(tools_by_tag.keys())}")
    print(f"Tools by tag: {tools_by_tag}")
    print(f"Tools registered: {list(tools.keys())}")
    print(f"Terminate tool present: {'terminate' in tools}")
    print()


def test_specialized_registries():
    """Test creating specialized agent registries."""
    print("=== Specialized Registry Test ===")

    # Test different registry configurations
    configs = {
        "Basic File Operations": PythonActionRegistry(tags=["file_operations"]),
        "Search Focused": PythonActionRegistry(tags=["search"]),
        "Read Only": PythonActionRegistry(tags=["read"]),
        "Complete System": PythonActionRegistry(tags=["file_operations", "system"])
    }

    for name, registry in configs.items():
        actions = registry.get_actions()
        action_names = [action.name for action in actions]
        print(f"{name}: {len(actions)} tools - {action_names}")
    print()


def create_readme_agent(model: str = "gpt-4o"):
    """Create an agent specialized for README generation."""
    goals = [
        Goal(priority=1,
             name="Gather Information",
             description="Read each file in the project in order to build a deep understanding of the project in order to write a README"),
        Goal(priority=2,
             name="Terminate",
             description="Call terminate when done and provide a complete README for the project in the message parameter")
    ]

    # Terminate auto-registers with "system" tag
    action_registry = PythonActionRegistry(tags=["file_operations", "system"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=lambda prompt: generate_response(prompt, model=model),
        environment=Environment()
    )


def create_file_analysis_agent(model: str = "gpt-4o"):
    """Create an agent specialized for file analysis."""
    goals = [
        Goal(priority=1,
             name="File Analysis",
             description="Analyze the project structure and file contents to understand the codebase organization"),
        Goal(priority=2,
             name="Report Findings",
             description="Provide a summary of findings and terminate with analysis results")
    ]

    # Terminate auto-registers with "system" tag
    action_registry = PythonActionRegistry(tags=["search", "file_operations", "system"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=lambda prompt: generate_response(prompt, model=model),
        environment=Environment()
    )


def test_agent_creation_with_different_models():
    """Test that agents can be created with different model configurations."""
    print("=== LLM Provider Test ===")

    # Test different model configurations
    models_to_test = [
        "gpt-4o",  # OpenAI
        "gpt-4o-mini",  # OpenAI (cheaper)
        # "claude-3-sonnet-20240229",          # Anthropic (uncomment if you have API key)
        # "gemini-pro",                        # Google (uncomment if you have API key)
    ]

    for model in models_to_test:
        try:
            agent = create_readme_agent(model=model)
            print(f"✅ {model}: Agent created successfully")
        except Exception as e:
            print(f"❌ {model}: Failed - {str(e)}")
    print()


def test_actual_llm_calls():
    """Test that LLMs actually respond to prompts."""
    models_to_test = ["gpt-4o", "gpt-4o-mini"]

    for model in models_to_test:
        try:
            # Create simple test prompt
            test_prompt = Prompt(messages=[{"role": "user", "content": "Say 'test'"}])
            response = generate_response(test_prompt, model=model)

            assert len(response) > 0
            print(f"✅ {model}: LLM responded successfully")
        except Exception as e:
            print(f"❌ {model}: LLM call failed - {str(e)}")


def run_demo_agent():
    """Run a demo agent to test the complete system."""
    print("=== Demo Agent Execution ===")

    # Create a README generation agent
    agent = create_readme_agent()

    # Show agent configuration
    actions = agent.actions.get_actions()
    registry_info = [action.name for action in actions]
    print(f"Agent has {len(registry_info)} tools available: {registry_info}")
    print()

    # Uncomment to actually run the agent (requires API key)
    # print("Running agent to generate README...")
    # memory = agent.run("Analyze this project and create a comprehensive README", max_iterations=5)
    # print("Agent execution completed!")
    # print(f"Final result: {memory.get_memories()[-1] if memory.get_memories() else 'No result'}")

    print("(Agent execution commented out - requires LLM API key)")
    print("To run: Uncomment the lines above and ensure you have an API key set")


def main():
    """Main test function."""
    print("🚀 Enhanced File Explorer Agent System Test\n")

    # Run all tests
    test_tool_discovery()
    test_specialized_registries()
    test_llm_agnostic_functionality()
    run_demo_agent()

    print("✅ All tests completed!")
    print("\n🎯 Your enhanced agent system is ready for use!")
    print("\nKey improvements implemented:")
    print("- ✅ Decorator-based tool registration")
    print("- ✅ Tag-based tool organization")
    print("- ✅ Specialized agent creation")
    print("- ✅ LLM-agnostic design")
    print("- ✅ Enhanced core framework")


if __name__ == "__main__":
    main()