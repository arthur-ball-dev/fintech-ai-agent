#!/usr/bin/env python3
"""
Example script showing how to use the File Explorer Agent
"""
import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.agents.file_explorer.agent import create_file_explorer_agent

def main():
    # Create the agent
    agent = create_file_explorer_agent()
    
    # Example tasks
    tasks = [
        "Write a README for this project.",
        "Analyze the code structure and suggest improvements.",
        "Create a summary of all Python files in the project."
    ]
    
    print("File Explorer Agent")
    print("=" * 50)
    print("Available tasks:")
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
    
    # Run the agent
    final_memory = agent.run(user_input)
    
    # Display results
    print("\n" + "=" * 50)
    print("Task completed!")
    
    # Optionally save the conversation history
    save = input("\nSave conversation history? (y/n): ")
    if save.lower() == 'y':
        import json
        with open('conversation_history.json', 'w') as f:
            json.dump(final_memory.get_memories(), f, indent=2)
        print("Conversation saved to conversation_history.json")

if __name__ == "__main__":
    main()