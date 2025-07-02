"""
Example script showing how to use the Enhanced File Explorer Agent System
with Multi-Provider LLM Support
"""
import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.agents.file_explorer.agent import create_file_explorer_agent, create_readme_agent, \
    create_analysis_agent
from src.framework.llm.client import LLMClient


def display_header():
    """Display professional application header"""
    print("🤖 Enhanced File Explorer Agent System")
    print("=" * 60)
    print("Multi-Provider LLM Support | Enterprise-Grade AI Agents")
    print("=" * 60)


def select_llm_provider():
    """
    Interactive LLM provider selection with status display

    Returns:
        tuple: (provider_name, model_type) or (None, None) if no providers available
    """
    try:
        client = LLMClient()
        status = client.get_provider_status()

        print("\n🔧 LLM Provider Configuration")
        print("-" * 40)

        # Display provider status
        available_providers = []
        provider_display = {}

        for i, (provider, info) in enumerate(status.items(), 1):
            emoji = "✅" if info['available'] else "❌"
            default_indicator = " (Default)" if info['is_default'] else ""
            status_text = "Ready" if info['available'] else "No API Key"

            print(f"{i}. {emoji} {provider.title()}{default_indicator} - {status_text}")

            if info['available']:
                available_providers.append(provider)
                provider_display[i] = provider

                # Show available model tiers
                models = info['models']
                print(f"   📊 Fast: {models.get('fast', 'N/A')}")
                print(f"   🎯 Default: {models.get('default', 'N/A')}")
                print(f"   🚀 Advanced: {models.get('advanced', 'N/A')}")

        if not available_providers:
            print("\n⚠️  No LLM providers configured!")
            print("Please set up your API keys:")
            print("   - OPENAI_API_KEY (for OpenAI/GPT models)")
            print("   - ANTHROPIC_API_KEY (for Anthropic/Claude models)")
            return None, None

        # Auto-select if only one provider
        if len(available_providers) == 1:
            selected_provider = available_providers[0]
            print(f"\n🎯 Auto-selecting: {selected_provider.title()}")
        else:
            # User selection
            try:
                choice = input(f"\nSelect provider (1-{len(status)}): ").strip()
                if not choice:
                    # Default to first available
                    selected_provider = available_providers[0]
                    print(f"Using default: {selected_provider.title()}")
                else:
                    choice_num = int(choice)
                    if choice_num in provider_display:
                        selected_provider = provider_display[choice_num]
                    else:
                        selected_provider = available_providers[0]
                        print(f"Invalid selection. Using: {selected_provider.title()}")
            except ValueError:
                selected_provider = available_providers[0]
                print(f"Invalid input. Using: {selected_provider.title()}")

        # Model tier selection
        print(f"\n🎛️  Model Performance Tiers for {selected_provider.title()}:")
        print("1. ⚡ Fast - Quick responses, lower cost")
        print("2. 🎯 Default - Balanced performance (Recommended)")
        print("3. 🚀 Advanced - Highest quality, higher cost")

        tier_map = {1: 'fast', 2: 'default', 3: 'advanced'}
        try:
            tier_choice = input("Select model tier (1-3, default=2): ").strip()
            if not tier_choice:
                model_type = 'default'
            else:
                tier_num = int(tier_choice)
                model_type = tier_map.get(tier_num, 'default')
        except ValueError:
            model_type = 'default'

        print(f"✅ Selected: {selected_provider.title()} ({model_type} tier)")
        return selected_provider, model_type

    except Exception as e:
        print(f"❌ Error configuring LLM provider: {str(e)}")
        return None, None


def select_agent_and_task():
    """Agent and task selection interface"""
    print("\n🤖 Agent Selection")
    print("-" * 40)

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
        print(f"{num}. 📋 {name}")
        print(f"   {description}")

    # Get agent choice
    try:
        agent_choice = input(f"\nSelect agent type (1-3, default=1): ").strip()
        if not agent_choice:
            agent_choice = 1
        else:
            agent_choice = int(agent_choice)
        if agent_choice not in agent_types:
            agent_choice = 1
    except ValueError:
        agent_choice = 1

    agent_name, agent_creator, _ = agent_types[agent_choice]
    print(f"✅ Selected: {agent_name}")

    # Task selection
    print(f"\n📋 Task Selection")
    print("-" * 40)

    tasks = [
        "Write a comprehensive README for this project.",
        "Analyze the code structure and suggest improvements.",
        "Create a summary of all Python files in the project.",
        "Generate documentation for the new LLM provider system.",
        "Review the project for FinTech industry best practices."
    ]

    print("Available tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print(f"{len(tasks) + 1}. 💭 Custom task")

    # Get task choice
    choice = input(f"\nSelect a task (1-{len(tasks) + 1}) or enter custom task: ").strip()

    try:
        task_index = int(choice) - 1
        if 0 <= task_index < len(tasks):
            user_input = tasks[task_index]
        else:
            user_input = input("Enter your custom task: ").strip()
    except ValueError:
        if choice:
            user_input = choice
        else:
            user_input = tasks[0]  # Default task

    return agent_creator, agent_name, user_input


def execute_agent_task(agent_creator, agent_name, user_input, provider, model_type):
    """Execute the selected agent task with specified LLM provider"""
    print(f"\n🚀 Executing Task")
    print("=" * 60)
    print(f"Agent: {agent_name}")
    print(f"LLM Provider: {provider.title()} ({model_type} tier)")
    print(f"Task: {user_input}")
    print("=" * 60)

    try:
        # Create the agent
        agent = agent_creator()

        # Show agent capabilities
        actions = agent.actions.get_actions()
        registry_info = [action.name for action in actions]
        print(f"🛠️  Agent capabilities: {len(registry_info)} tools available")
        print(f"Tools: {', '.join(registry_info)}")
        print()

        # Execute the task
        # Note: You may need to modify agent creation to accept LLM provider settings
        # This depends on your agent architecture
        final_memory = agent.run(user_input)

        # Display results
        print("\n" + "=" * 60)
        print("✅ Task Completed!")
        print("=" * 60)

        # Show final result
        memories = final_memory.get_memories()
        if memories:
            final_result = memories[-1]
            result_type = final_result.get('type', 'unknown')
            content_preview = str(final_result.get('content', ''))[:200]

            print(f"📊 Result type: {result_type}")
            print(f"📝 Content preview: {content_preview}...")

            if len(content_preview) >= 200:
                print("   [Content truncated - see full output above]")

        return final_memory

    except Exception as e:
        print(f"❌ Task execution failed: {str(e)}")
        return None


def save_conversation_history(final_memory):
    """Optionally save conversation history"""
    if not final_memory:
        return

    save = input("\n💾 Save conversation history? (y/n, default=n): ").strip().lower()
    if save in ['y', 'yes']:
        try:
            import json
            filename = 'conversation_history.json'
            with open(filename, 'w') as f:
                json.dump(final_memory.get_memories(), f, indent=2)
            print(f"✅ Conversation saved to {filename}")
        except Exception as e:
            print(f"❌ Failed to save conversation: {str(e)}")


def main():
    """Main application flow"""
    display_header()

    # Step 1: Configure LLM provider
    provider, model_type = select_llm_provider()
    if not provider:
        print("\n❌ Cannot proceed without LLM provider. Exiting.")
        return

    # Step 2: Select agent and task
    agent_creator, agent_name, user_input = select_agent_and_task()

    # Step 3: Execute task
    final_memory = execute_agent_task(agent_creator, agent_name, user_input, provider, model_type)

    # Step 4: Optional save
    save_conversation_history(final_memory)

    print(f"\n🎯 Session complete! Thank you for using the Enhanced File Explorer Agent System.")


if __name__ == "__main__":
    main()