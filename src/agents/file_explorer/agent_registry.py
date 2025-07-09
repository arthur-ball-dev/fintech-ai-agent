"""
Agent Registry and Selection Utilities

Provides helper functions for discovering, selecting, and configuring
agents based on use case requirements and analysis preferences.
"""
from typing import Dict, Any
from src.framework.core.agent import Agent

# Import all agent creation functions
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

def get_available_agents() -> Dict[str, Dict[str, Any]]:
    """
    Return available agent options for interactive selection.
    Organized by capability level with most impressive agents first.
    """
    return {
        # Specialized FinTech agents (most impressive)
        "risk_management": {
            "name": "Risk Management Agent",
            "description": "Pattern-based financial risk analysis and control assessment",
            "factory": create_risk_management_agent,
            "use_case": "Analyzing trading system risk controls and safety mechanisms",
            "analysis_type": "Pattern-Based",
            "category": "FinTech Specialized"
        },
        "performance": {
            "name": "Performance Optimization Agent",
            "description": "Pattern-based high-frequency trading performance analysis",
            "factory": create_performance_agent,
            "use_case": "Identifying performance bottlenecks and optimization opportunities",
            "analysis_type": "Pattern-Based",
            "category": "FinTech Specialized"
        },
        "compliance": {
            "name": "Compliance & Security Agent",
            "description": "Pattern-based regulatory compliance and security assessment",
            "factory": create_compliance_agent,
            "use_case": "Evaluating regulatory compliance and security best practices",
            "analysis_type": "Pattern-Based",
            "category": "FinTech Specialized"
        },
        "architecture": {
            "name": "FinTech Architecture Agent",
            "description": "Pattern-based enterprise architecture and scalability analysis",
            "factory": create_architecture_agent,
            "use_case": "Assessing system architecture and scalability patterns",
            "analysis_type": "Pattern-Based",
            "category": "FinTech Specialized"
        },
        "comprehensive": {
            "name": "Comprehensive FinTech Agent",
            "description": "Complete pattern-based analysis across all FinTech domains",
            "factory": create_comprehensive_fintech_agent,
            "use_case": "Full technical demonstration across all capabilities",
            "analysis_type": "Pattern-Based",
            "category": "FinTech Specialized"
        },
        
        # Hybrid analysis agents (most sophisticated)
        "hybrid_risk": {
            "name": "Hybrid Risk Management Agent",
            "description": "Pattern + AI-powered risk analysis with business context",
            "factory": create_hybrid_risk_management_agent,
            "use_case": "Deep risk assessment with AI insights and business impact analysis",
            "analysis_type": "Hybrid (Pattern + AI-Powered)",
            "category": "Hybrid Analysis"
        },
        "hybrid_compliance": {
            "name": "Hybrid Compliance Agent",
            "description": "Pattern + AI-powered compliance analysis with regulatory context",
            "factory": create_hybrid_compliance_agent,
            "use_case": "Comprehensive compliance assessment with AI-powered regulatory insights",
            "analysis_type": "Hybrid (Pattern + AI-Powered)",
            "category": "Hybrid Analysis"
        },
        "hybrid_performance": {
            "name": "Hybrid Performance Agent",
            "description": "Pattern + AI-powered performance analysis with optimization context",
            "factory": create_hybrid_performance_agent,
            "use_case": "Advanced performance optimization with AI-driven insights",
            "analysis_type": "Hybrid (Pattern + AI-Powered)",
            "category": "Hybrid Analysis"
        },
        "hybrid_comprehensive": {
            "name": "Hybrid Comprehensive Agent",
            "description": "Complete pattern + AI-powered analysis across all domains",
            "factory": create_hybrid_comprehensive_agent,
            "use_case": "Maximum depth analysis combining technical patterns with business intelligence",
            "analysis_type": "Hybrid (Pattern + AI-Powered)",
            "category": "Hybrid Analysis"
        },
        
        # Basic utility agents
        "file_explorer": {
            "name": "Enhanced File Explorer Agent",
            "description": "General-purpose exploration with FinTech pattern recognition",
            "factory": create_file_explorer_agent,
            "use_case": "General code analysis with financial pattern awareness",
            "analysis_type": "Basic",
            "category": "Basic Utilities"
        },
        "readme": {
            "name": "FinTech Documentation Agent",
            "description": "Professional README generation highlighting technical capabilities",
            "factory": create_readme_agent,
            "use_case": "Creating professional documentation for project portfolios",
            "analysis_type": "Basic",
            "category": "Basic Utilities"
        },
        "code_analysis": {
            "name": "Technical Code Analysis Agent",
            "description": "Comprehensive code analysis with architectural insights",
            "factory": create_code_analysis_agent,
            "use_case": "Demonstrating technical analysis and code review capabilities",
            "analysis_type": "Basic",
            "category": "Basic Utilities"
        }
    }

def get_agents_by_category() -> Dict[str, Dict[str, Any]]:
    """
    Return agents organized by category for structured selection.
    """
    agents = get_available_agents()
    categories = {}
    
    for agent_key, agent_info in agents.items():
        category = agent_info["category"]
        if category not in categories:
            categories[category] = {}
        categories[category][agent_key] = agent_info
    
    return categories

def create_agent_for_use_case(use_case: str, analysis_mode: str = "pattern") -> Agent:
    """
    Create an agent optimized for specific use cases with chosen analysis mode.
    
    Args:
        use_case: Type of analysis needed
                 - "trading_systems": Focus on performance and risk management
                 - "compliance_review": Focus on regulatory and security compliance
                 - "architecture_review": Focus on system design and scalability
                 - "technical_assessment": Comprehensive technical evaluation
        analysis_mode: Analysis approach
                      - "pattern": Pattern-based only (fast, consistent)
                      - "hybrid": Pattern + AI-powered (comprehensive, contextual)
    
    Returns:
        Configured agent for the specific use case and analysis mode
    """
    # Pattern-based mappings
    pattern_mapping = {
        "trading_systems": create_performance_agent,
        "compliance_review": create_compliance_agent,
        "architecture_review": create_architecture_agent,
        "technical_assessment": create_comprehensive_fintech_agent
    }
    
    # Hybrid analysis mappings
    hybrid_mapping = {
        "trading_systems": create_hybrid_performance_agent,
        "compliance_review": create_hybrid_compliance_agent,
        "architecture_review": create_architecture_agent,  # No hybrid version yet
        "technical_assessment": create_hybrid_comprehensive_agent
    }
    
    if analysis_mode == "hybrid":
        factory = hybrid_mapping.get(use_case, create_hybrid_comprehensive_agent)
    else:
        factory = pattern_mapping.get(use_case, create_comprehensive_fintech_agent)
    
    return factory()

def get_analysis_mode_info() -> Dict[str, Dict[str, Any]]:
    """
    Return information about available analysis modes.
    """
    return {
        "pattern": {
            "name": "Pattern-Based Analysis",
            "description": "Fast, consistent, audit-friendly analysis using predefined patterns",
            "benefits": ["Consistent results", "Fast execution", "Audit trail", "No additional LLM costs"],
            "use_cases": ["Baseline assessment", "Automated scanning", "Compliance audits"],
            "agents": ["risk_management", "performance", "compliance", "architecture", "comprehensive"]
        },
        "hybrid": {
            "name": "Hybrid Analysis (Pattern + AI-Powered)",
            "description": "Comprehensive analysis combining pattern detection with AI-powered contextual insights",
            "benefits": ["Deep insights", "Business context", "Novel risk identification", "Strategic guidance"],
            "use_cases": ["Strategic planning", "Comprehensive reviews", "Complex assessments"],
            "agents": ["hybrid_risk", "hybrid_compliance", "hybrid_performance", "hybrid_comprehensive"]
        },
        "basic": {
            "name": "Basic Utility Operations",
            "description": "General-purpose file operations and documentation with FinTech awareness",
            "benefits": ["Simple usage", "General purpose", "Documentation focus", "Quick results"],
            "use_cases": ["File exploration", "README generation", "Basic code analysis"],
            "agents": ["file_explorer", "readme", "code_analysis"]
        }
    }

def get_recommended_agent(requirements: Dict[str, Any]) -> str:
    """
    Get recommended agent based on user requirements.
    
    Args:
        requirements: Dictionary with analysis requirements
                     - "domain": "fintech", "general", "documentation"
                     - "complexity": "basic", "advanced", "comprehensive"
                     - "speed_priority": bool (True for fast results)
                     - "depth_priority": bool (True for deep insights)
    
    Returns:
        Recommended agent key
    """
    domain = requirements.get("domain", "general")
    complexity = requirements.get("complexity", "basic")
    speed_priority = requirements.get("speed_priority", True)
    depth_priority = requirements.get("depth_priority", False)
    
    # Documentation focus
    if domain == "documentation":
        return "readme"
    
    # Basic general analysis
    if domain == "general" or complexity == "basic":
        return "file_explorer"
    
    # FinTech domain
    if domain == "fintech":
        if complexity == "comprehensive":
            if depth_priority and not speed_priority:
                return "hybrid_comprehensive"
            else:
                return "comprehensive"
        elif complexity == "advanced":
            if depth_priority and not speed_priority:
                return "hybrid_risk"  # Most sophisticated single-domain agent
            else:
                return "risk_management"  # Most impressive single-domain agent
        else:
            return "compliance"  # Good starting point for FinTech
    
    # Default fallback
    return "code_analysis"

def list_available_agents() -> None:
    """
    Print a formatted list of all available agents organized by category.
    """
    categories = get_agents_by_category()
    
    print("🤖 Available FinTech AI Agents")
    print("=" * 50)
    
    for category_name, agents in categories.items():
        print(f"\n📂 {category_name}:")
        print("-" * 30)
        
        for agent_key, agent_info in agents.items():
            print(f"🔹 {agent_info['name']}")
            print(f"   Key: {agent_key}")
            print(f"   Type: {agent_info['analysis_type']}")
            print(f"   Use Case: {agent_info['use_case']}")
            print()

def create_agent_by_key(agent_key: str) -> Agent:
    """
    Create an agent by its registry key.
    
    Args:
        agent_key: Key from get_available_agents()
    
    Returns:
        Configured agent instance
    
    Raises:
        KeyError: If agent_key is not found
    """
    agents = get_available_agents()
    
    if agent_key not in agents:
        available_keys = list(agents.keys())
        raise KeyError(f"Agent '{agent_key}' not found. Available agents: {available_keys}")
    
    factory = agents[agent_key]["factory"]
    return factory()