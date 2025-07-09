"""
Enhanced File Explorer Agent System with Progressive Task Selection
Multi-Provider LLM Support | Enterprise-Grade AI Agents | Better UX
"""
import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Import from the modular structure - CORRECTED IMPORT
from src.agents.file_explorer.progressive_agent_selection import (
    run_progressive_task_selection,
    display_selection_summary
)
from src.agents.file_explorer.agent_registry import create_agent_by_key
from src.framework.llm.client import LLMClient


def display_header():
    """Display professional application header"""
    print("🤖 Enhanced FinTech AI Agent System")
    print("=" * 60)
    print("Multi-Provider LLM | Progressive Selection | Enterprise-Grade")
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


def execute_agent_task(selection_result, provider, model_type):
    """Execute the selected agent task with specified LLM provider"""
    print(f"\n🚀 Executing FinTech Analysis Task")
    print("=" * 70)
    print(f"Agent: {selection_result['agent_name']}")
    print(f"Category: {selection_result['category']}")
    print(f"LLM Provider: {provider.title()} ({model_type} tier)")
    print(f"Task: {selection_result['task']}")

    if selection_result.get('use_hybrid'):
        print(f"Analysis Mode: Hybrid (Pattern + AI-Powered)")
    else:
        print(f"Analysis Mode: Pattern-Based")

    print("=" * 70)

    try:
        # Create the agent using the registry system
        agent = create_agent_by_key(selection_result['agent_key'])

        # Show agent capabilities
        actions = agent.actions.get_actions()
        registry_info = [action.name for action in actions]
        print(f"🛠️  Agent capabilities: {len(registry_info)} tools available")

        # Show FinTech-specific tools if available
        fintech_tools = [tool for tool in registry_info if any(keyword in tool.lower() for keyword in
                                                               ['fintech', 'risk', 'compliance',
                                                                'performance', 'architecture', 'analyze'])]

        if fintech_tools:
            print(f"🏦 FinTech Analysis Tools: {len(fintech_tools)} specialized tools")
            # Show first few tools as examples
            sample_tools = fintech_tools[:3]
            if len(fintech_tools) > 3:
                sample_tools.append(f"... and {len(fintech_tools) - 3} more")
            print(f"   Examples: {', '.join(sample_tools)}")

        print(f"📋 All Available Tools: {', '.join(registry_info)}")
        print()

        # Execute the task
        print("🔄 Starting agent execution...")
        print(f"💡 The agent will analyze your project using {selection_result['category']} approach")
        print()

        final_memory = agent.run(selection_result['task'])

        # Display results
        print("\n" + "=" * 70)
        print("✅ FinTech Analysis Completed!")
        print("=" * 70)

        # Show final result
        memories = final_memory.get_memories()
        if memories:
            final_result = memories[-1]
            result_type = final_result.get('type', 'unknown')
            content = str(final_result.get('content', ''))

            print(f"📊 Result type: {result_type}")
            print(f"📝 Content length: {len(content)} characters")

            # Show preview for very long results
            if len(content) > 1000:
                print(f"📄 Analysis Preview:")
                print("-" * 50)
                # Show first 800 characters
                preview = content[:800]
                # Try to cut at a sensible point (end of sentence or line)
                if '.' in preview[-100:]:
                    cut_point = preview.rfind('.', -100) + 1
                    preview = preview[:cut_point]
                elif '\n' in preview[-100:]:
                    cut_point = preview.rfind('\n', -100)
                    preview = preview[:cut_point]

                print(preview)
                print(f"\n... [Analysis continues - full results shown above during execution]")
                print(f"📏 Total analysis length: {len(content)} characters")
            else:
                print(f"📄 Complete Analysis:")
                print("-" * 50)
                print(content)

        return final_memory

    except Exception as e:
        print(f"❌ Task execution failed: {str(e)}")
        print(f"🔧 This might be due to missing LLM API keys or configuration issues.")
        print(f"💡 Check that your API keys are properly configured.")
        return None


def save_conversation_history(final_memory, selection_result):
    """Optionally save conversation history with descriptive filename"""
    if not final_memory:
        return

    save = input("\n💾 Save FinTech analysis results? (y/n, default=n): ").strip().lower()
    if save in ['y', 'yes']:
        try:
            import json
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            agent_type = selection_result['agent_key'].replace('_', '-')
            analysis_mode = 'hybrid' if selection_result.get('use_hybrid') else 'pattern'

            filename = f'fintech-analysis_{agent_type}_{analysis_mode}_{timestamp}.json'

            # Save with metadata
            analysis_data = {
                'metadata': {
                    'agent_name': selection_result['agent_name'],
                    'agent_key': selection_result['agent_key'],
                    'category': selection_result['category'],
                    'task': selection_result['task'],
                    'analysis_mode': 'Hybrid (Pattern + AI)' if selection_result.get('use_hybrid') else 'Pattern-Based',
                    'timestamp': datetime.now().isoformat(),
                    'export_version': '1.0'
                },
                'conversation_history': final_memory.get_memories()
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Analysis results saved to {filename}")
            print(f"   📁 File includes metadata and complete conversation history")

        except Exception as e:
            print(f"❌ Failed to save results: {str(e)}")


def display_startup_info():
    """Display helpful startup information"""
    print("\n💡 Getting Started:")
    print("   1. First, configure your LLM provider (OpenAI or Anthropic)")
    print("   2. Choose your analysis focus (FinTech or Utilities)")
    print("   3. Select specific agent and task")
    print("   4. Choose analysis depth (Pattern-based or Hybrid)")
    print("   5. Watch your agent perform sophisticated FinTech analysis!")
    print()
    print("🎯 This system demonstrates enterprise-grade AI capabilities")
    print("   suitable for financial services applications.")


def main():
    """Main application flow with progressive task selection"""
    display_header()
    display_startup_info()

    # Step 1: Configure LLM provider
    provider, model_type = select_llm_provider()
    if not provider:
        print("\n❌ Cannot proceed without LLM provider. Exiting.")
        print("💡 Please configure OPENAI_API_KEY or ANTHROPIC_API_KEY and try again.")
        return

    # Steps 2-5: Progressive task selection
    try:
        selection_result = run_progressive_task_selection()

        # Display final selection summary
        display_selection_summary(selection_result)

        # Confirm execution
        print(f"\n🚀 Ready to execute analysis!")
        confirm = input("Proceed with analysis? (y/n, default=y): ").strip().lower()

        if confirm in ['n', 'no']:
            print("Analysis cancelled. Thank you for using the FinTech AI Agent System!")
            return

    except KeyboardInterrupt:
        print("\n\n⏹️  Task selection cancelled by user.")
        return
    except Exception as e:
        print(f"\n❌ Error during task selection: {str(e)}")
        return

    # Step 6: Execute the selected analysis
    try:
        final_memory = execute_agent_task(selection_result, provider, model_type)

        # Step 7: Optional save
        save_conversation_history(final_memory, selection_result)

        print(f"\n🎯 FinTech Analysis Complete!")
        print("=" * 50)
        print("Thank you for using the Enhanced FinTech AI Agent System.")
        print("This demonstration showcases enterprise-grade AI capabilities")
        print("for financial technology applications.")

    except KeyboardInterrupt:
        print("\n\n⏹️  Analysis interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error during execution: {str(e)}")
        print("💡 Please check your configuration and try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thank you for using the FinTech AI Agent System.")
    except Exception as e:
        print(f"\n💥 System error: {str(e)}")
        print("Please check your installation and configuration.")