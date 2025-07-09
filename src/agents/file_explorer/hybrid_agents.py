"""
Hybrid Analysis Agents (Pattern + AI-Powered Contextual Analysis)

These agents combine deterministic pattern-based detection with AI-powered 
contextual analysis for maximum insight depth and business understanding.
Agents always use LLM for decision-making, with AI-powered contextual 
analysis for deeper code insights.
"""
from src.framework.core.goals import Goal
from src.framework.core.agent import Agent
from src.framework.actions.registry import PythonActionRegistry
from src.framework.language.function_calling import AgentFunctionCallingActionLanguage
from src.framework.environment.environment import Environment
from src.framework.llm.client import generate_response
from . import actions  # This imports and registers all decorated functions

def create_hybrid_risk_management_agent() -> Agent:
    """
    Create a hybrid risk management agent that combines pattern-based detection
    with AI-powered contextual analysis for comprehensive risk assessment.
    """
    goals = [
        Goal(
            priority=1,
            name="Hybrid Risk Analysis",
            description="Perform comprehensive risk analysis using both pattern-based detection and AI-powered contextual analysis to identify risk management patterns and provide business context."
        ),
        Goal(
            priority=2,
            name="Contextual Risk Assessment",
            description="Use AI analysis to identify additional risk factors not captured by pattern matching and assess business impact in financial trading contexts."
        ),
        Goal(
            priority=3,
            name="Integrated Risk Report",
            description="Generate a comprehensive risk report that combines deterministic findings with AI insights for complete risk assessment."
        ),
        Goal(
            priority=4,
            name="Terminate",
            description="Provide an integrated risk assessment that demonstrates both technical pattern recognition and business context understanding."
        )
    ]

    action_registry = PythonActionRegistry(tags=["fintech", "risk_management", "file_operations", "system"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )

def create_hybrid_compliance_agent() -> Agent:
    """
    Create a hybrid compliance agent that combines pattern-based security scanning
    with AI-powered contextual analysis for comprehensive regulatory assessment.
    """
    goals = [
        Goal(
            priority=1,
            name="Hybrid Compliance Analysis",
            description="Perform comprehensive compliance analysis using both pattern-based security scanning and AI-powered contextual analysis to identify regulatory requirements and business implications."
        ),
        Goal(
            priority=2,
            name="Contextual Regulatory Assessment",
            description="Use AI analysis to identify additional compliance considerations and assess regulatory impact in financial services context."
        ),
        Goal(
            priority=3,
            name="Integrated Compliance Report",
            description="Generate a comprehensive compliance report that combines deterministic security findings with AI-powered regulatory insights."
        ),
        Goal(
            priority=4,
            name="Terminate",
            description="Provide an integrated compliance assessment suitable for both technical teams and regulatory review."
        )
    ]

    action_registry = PythonActionRegistry(tags=["fintech", "compliance", "security", "file_operations", "system"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )

def create_hybrid_performance_agent() -> Agent:
    """
    Create a hybrid performance agent that combines pattern-based optimization detection
    with AI-powered contextual analysis for comprehensive performance assessment.
    """
    goals = [
        Goal(
            priority=1,
            name="Hybrid Performance Analysis",
            description="Perform comprehensive performance analysis using both pattern-based optimization detection and AI-powered contextual analysis for trading system performance."
        ),
        Goal(
            priority=2,
            name="Contextual Optimization Assessment",
            description="Use AI analysis to identify additional performance considerations and assess optimization impact in high-frequency trading contexts."
        ),
        Goal(
            priority=3,
            name="Integrated Performance Report",
            description="Generate a comprehensive performance report that combines deterministic optimization findings with AI-powered performance insights."
        ),
        Goal(
            priority=4,
            name="Terminate",
            description="Provide an integrated performance assessment for high-frequency trading system optimization."
        )
    ]

    action_registry = PythonActionRegistry(tags=["fintech", "performance", "file_operations", "system"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )

def create_hybrid_comprehensive_agent() -> Agent:
    """
    Create a comprehensive hybrid agent that combines all FinTech capabilities
    with AI-powered contextual analysis for maximum insight depth.
    """
    goals = [
        Goal(
            priority=1,
            name="Hybrid Comprehensive Analysis",
            description="Perform complete analysis covering all FinTech domains using both pattern-based detection and AI-powered contextual analysis for maximum insight depth."
        ),
        Goal(
            priority=2,
            name="Integrated Cross-Domain Assessment",
            description="Integrate pattern-based findings with AI insights across risk management, performance, compliance, and architecture domains."
        ),
        Goal(
            priority=3,
            name="Strategic Business Context",
            description="Provide strategic recommendations that combine technical findings with business context and regulatory implications."
        ),
        Goal(
            priority=4,
            name="Terminate",
            description="Provide a comprehensive hybrid analysis report that demonstrates both technical pattern recognition and strategic business understanding."
        )
    ]

    # Include ALL FinTech analysis capabilities
    action_registry = PythonActionRegistry(tags=[
        "fintech", "risk_management", "performance", "compliance", 
        "security", "architecture", "comprehensive", "analysis",
        "file_operations", "search", "system"
    ])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )