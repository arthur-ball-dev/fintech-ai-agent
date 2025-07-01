"""
Example script showing how to use the Enhanced File Explorer Agent System
"""
import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.agents.file_explorer.agent import create_file_explorer_agent, create_readme_agent, \
    create_analysis_agent


def main():
    print("Enhanced File Explorer Agent System")
    print("=" * 50)

    # Agent types
    agent_types = {
        1: ("File Explorer Agent", create_file_explorer_agent,
            "General file exploration and documentation"),
        2: ("README Generator Agent", create_readme_agent,
            "Specialized for creating comprehensive README files"),
        3: ("Code Analysis Agent", create_analysis_agent,
            "Focused on code structure analysis and recommendations")
    }

    print("Available agent types:")
    for num, (name, _, description) in agent_types.items():
        print(f"{num}. {name} - {description}")

    # Get agent choice
    try:
        agent_choice = int(input("\nSelect agent type (1-3): "))
        if agent_choice not in agent_types:
            agent_choice = 1
    except ValueError:
        agent_choice = 1

    agent_name, agent_creator, _ = agent_types[agent_choice]
    print(f"\nUsing: {agent_name}")

    # Example tasks
    tasks = [
        "Write a comprehensive README for this project.",
        "Analyze the code structure and suggest improvements.",
        "Create a summary of all Python files in the project.",
        "Generate documentation for the new decorator system."
    ]

    print("\nAvailable tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print(f"{len(tasks) + 1}. Custom task")

    # Get user choice
    choice = input("\nSelect a task (number) or enter a custom task: ")

    try:
        task_index = int(choice) - 1
        if 0 <= task_index < len(tasks):
            user_input = tasks[task_index]
        else:
            user_input = input("Enter your custom task: ")
    except ValueError:
        user_input = choice

    print(f"\nExecuting task: {user_input}")
    print("=" * 50)

    # Create and run the agent
    agent = agent_creator()  # This calls the function to create the agent

    # Show agent capabilities
    actions = agent.actions.get_actions()
    registry_info = [action.name for action in actions]
    print(f"Agent capabilities: {len(registry_info)} tools available")
    print(f"Tools: {registry_info}")
    print()

    # Run the agent
    final_memory = agent.run(user_input)

    # Display results
    print("\n" + "=" * 50)
    print("Task completed!")

    # Show final result
    memories = final_memory.get_memories()
    if memories:
        final_result = memories[-1]
        print(f"\nFinal result type: {final_result.get('type', 'unknown')}")
        print(f"Content preview: {str(final_result.get('content', ''))[:200]}...")

    # Optionally save the conversation history
    save = input("\nSave conversation history? (y/n): ")
    if save.lower() == 'y':
        import json
        with open('conversation_history.json', 'w') as f:
            json.dump(final_memory.get_memories(), f, indent=2)
        print("Conversation saved to conversation_history.json")


if __name__ == "__main__":
    main()