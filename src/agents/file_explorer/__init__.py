"""
Agent Registry Integration for Progressive Selection System
Provides clean imports and ensures all agents are available
"""

# Import all agent factories
from .basic_agents import (
    create_file_explorer_agent,
    create_readme_agent,
    create_code_analysis_agent
)

from .fintech_agents import (
    create_risk_management_agent,
    create_performance_agent,
    create_compliance_agent,
    create_architecture_agent,
    create_comprehensive_fintech_agent
)

from .hybrid_agents import (
    create_hybrid_risk_management_agent,
    create_hybrid_compliance_agent,
    create_hybrid_performance_agent,
    create_hybrid_comprehensive_agent
)

# Import registry functions
from .agent_registry import (
    get_available_agents,
    get_agents_by_category,
    create_agent_by_key,
    get_analysis_mode_info,
    list_available_agents
)

# Import progressive selection system - CORRECTED IMPORT
from .progressive_agent_selection import (
    run_progressive_task_selection,
    display_selection_summary
)

# Define agent key mappings for progressive selection
AGENT_KEY_MAPPING = {
    # FinTech Specialized Agents (Pattern-Based)
    'risk_management': create_risk_management_agent,
    'performance': create_performance_agent,
    'compliance': create_compliance_agent,
    'architecture': create_architecture_agent,
    'comprehensive': create_comprehensive_fintech_agent,

    # Hybrid Agents (Pattern + AI)
    'hybrid_risk_management': create_hybrid_risk_management_agent,
    'hybrid_performance': create_hybrid_performance_agent,
    'hybrid_compliance': create_hybrid_compliance_agent,
    'hybrid_comprehensive': create_hybrid_comprehensive_agent,

    # Basic Utility Agents
    'readme': create_readme_agent,
    'code_analysis': create_code_analysis_agent,
    'file_explorer': create_file_explorer_agent,

    # Fallback mappings
    'custom': create_comprehensive_fintech_agent,
    'custom_utility': create_file_explorer_agent
}

def create_agent_by_key(agent_key: str):
    """
    Create an agent by its key from the progressive selection system

    Args:
        agent_key: The agent key from progressive selection

    Returns:
        Configured agent instance

    Raises:
        KeyError: If agent_key is not found
    """
    if agent_key not in AGENT_KEY_MAPPING:
        # Provide helpful error message
        available_keys = list(AGENT_KEY_MAPPING.keys())
        raise KeyError(
            f"Agent '{agent_key}' not found in progressive selection mapping. "
            f"Available agents: {available_keys}"
        )

    factory_function = AGENT_KEY_MAPPING[agent_key]
    return factory_function()

def validate_progressive_selection_setup():
    """
    Validate that all agent keys used in progressive selection have corresponding factories
    """
    print("🔍 Validating Progressive Selection Setup...")

    # Test each agent key
    errors = []
    for agent_key, factory in AGENT_KEY_MAPPING.items():
        try:
            agent = factory()
            print(f"✅ {agent_key}: Agent created successfully")
        except Exception as e:
            errors.append(f"❌ {agent_key}: Error - {str(e)}")

    if errors:
        print("\n⚠️  Validation Errors Found:")
        for error in errors:
            print(f"   {error}")
        return False
    else:
        print(f"\n✅ All {len(AGENT_KEY_MAPPING)} agents validated successfully!")
        return True

def get_agent_capabilities_summary():
    """
    Get a summary of all available agent capabilities for documentation
    """
    capabilities = {
        'FinTech Specialized Agents': {
            'risk_management': "Trading system risk controls and operational safeguards analysis",
            'performance': "High-frequency trading performance optimization and latency analysis",
            'compliance': "Financial services regulatory compliance (SOX, GDPR, PCI-DSS)",
            'architecture': "Enterprise architecture and scalability assessment",
            'comprehensive': "Complete analysis across all FinTech domains"
        },
        'Hybrid Analysis Agents': {
            'hybrid_risk_management': "Pattern + AI risk analysis with business context",
            'hybrid_performance': "Pattern + AI performance optimization with strategic insights",
            'hybrid_compliance': "Pattern + AI compliance analysis with regulatory interpretation",
            'hybrid_comprehensive': "Maximum depth analysis with AI strategic guidance"
        },
        'Basic Utility Agents': {
            'readme': "Professional documentation generation with FinTech focus",
            'code_analysis': "Code structure analysis with financial technology awareness",
            'file_explorer': "General file operations with FinTech pattern recognition"
        }
    }

    return capabilities

def display_agent_portfolio():
    """
    Display a professional summary of the agent portfolio for employers
    """
    print("🤖 FinTech AI Agent Portfolio")
    print("=" * 50)

    capabilities = get_agent_capabilities_summary()

    for category, agents in capabilities.items():
        print(f"\n📂 {category}:")
        print("-" * 30)

        for agent_key, description in agents.items():
            print(f"🔹 {agent_key.replace('_', ' ').title()}")
            print(f"   {description}")
            print()

    print(f"📊 Total Portfolio: {sum(len(agents) for agents in capabilities.values())} specialized agents")
    print("🎯 Demonstrates: Financial domain expertise, AI integration, enterprise architecture")

# Export key functions for external use
__all__ = [
    # Agent creation functions
    'create_agent_by_key',
    'AGENT_KEY_MAPPING',

    # Progressive selection system
    'run_progressive_task_selection',
    'display_selection_summary',

    # Registry functions
    'get_available_agents',
    'get_agents_by_category',
    'get_analysis_mode_info',

    # Validation and documentation
    'validate_progressive_selection_setup',
    'get_agent_capabilities_summary',
    'display_agent_portfolio'
]

if __name__ == "__main__":
    # Test the progressive selection setup
    print("🧪 Testing Progressive Selection Setup")
    print("=" * 50)

    # Validate all agents
    validation_success = validate_progressive_selection_setup()

    if validation_success:
        print("\n🎯 Progressive Selection System Ready!")

        # Display portfolio summary
        print()
        display_agent_portfolio()

        print("\n💡 To use: Run 'python src/examples/run_file_explorer.py'")
    else:
        print("\n❌ Setup validation failed. Please check agent imports.")