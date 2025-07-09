"""
Specialized FinTech Pattern-Based Agents

These agents provide domain-specific analysis for financial technology applications
using deterministic pattern matching for consistent, audit-friendly results.
"""
from src.framework.core.goals import Goal
from src.framework.core.agent import Agent
from src.framework.actions.registry import PythonActionRegistry
from src.framework.language.function_calling import AgentFunctionCallingActionLanguage
from src.framework.environment.environment import Environment
from src.framework.llm.client import generate_response
from . import actions  # This imports and registers all decorated functions

def create_risk_management_agent() -> Agent:
    """
    Create a specialized agent for financial risk management analysis.
    Uses pattern-based analysis for consistent risk assessment.
    """
    goals = [
        Goal(
            priority=1,
            name="Risk Pattern Analysis",
            description="Analyze the entire codebase for financial risk management patterns including position limits, stop losses, and operational safeguards using pattern-based detection."
        ),
        Goal(
            priority=2,
            name="Control Gap Assessment",
            description="Identify missing risk controls and provide specific recommendations for trading system safety and regulatory compliance."
        ),
        Goal(
            priority=3,
            name="Risk Report Generation",
            description="Generate a comprehensive risk management report highlighting current controls and improvement recommendations."
        ),
        Goal(
            priority=4,
            name="Terminate",
            description="Provide a detailed risk assessment report focusing on financial system safety and control mechanisms."
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

def create_performance_agent() -> Agent:
    """
    Create a specialized agent for high-frequency trading performance analysis.
    Uses pattern-based analysis for performance optimization assessment.
    """
    goals = [
        Goal(
            priority=1,
            name="Performance Pattern Analysis",
            description="Analyze the codebase for performance optimization patterns including latency-critical operations and efficiency improvements using deterministic pattern matching."
        ),
        Goal(
            priority=2,
            name="Bottleneck Identification",
            description="Identify performance bottlenecks and anti-patterns that could impact system performance in trading environments."
        ),
        Goal(
            priority=3,
            name="Optimization Recommendations",
            description="Provide specific recommendations for performance improvements and system optimization strategies."
        ),
        Goal(
            priority=4,
            name="Terminate",
            description="Provide a detailed performance analysis report with optimization recommendations for high-performance trading systems."
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

def create_compliance_agent() -> Agent:
    """
    Create a specialized agent for regulatory compliance and security analysis.
    Uses pattern-based analysis for audit-friendly compliance assessment.
    """
    goals = [
        Goal(
            priority=1,
            name="Security Pattern Assessment",
            description="Scan the codebase for security vulnerabilities and compliance patterns related to data protection and access controls using deterministic pattern matching."
        ),
        Goal(
            priority=2,
            name="Regulatory Analysis",
            description="Analyze compliance with financial regulations including audit logging, data encryption, and access management requirements."
        ),
        Goal(
            priority=3,
            name="Compliance Gap Identification",
            description="Identify compliance gaps and provide specific recommendations for meeting regulatory requirements."
        ),
        Goal(
            priority=4,
            name="Terminate",
            description="Provide a comprehensive compliance and security assessment report with remediation recommendations."
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

def create_architecture_agent() -> Agent:
    """
    Create a specialized agent for FinTech architecture analysis.
    Uses pattern-based analysis for system design evaluation.
    """
    goals = [
        Goal(
            priority=1,
            name="Architecture Pattern Analysis",
            description="Analyze the system architecture for scalability patterns, API design, and microservices implementation using pattern-based detection."
        ),
        Goal(
            priority=2,
            name="Technology Stack Evaluation",
            description="Evaluate technology choices and architectural decisions from a scalability and maintainability perspective."
        ),
        Goal(
            priority=3,
            name="Scalability Assessment",
            description="Assess the system's ability to handle enterprise-scale loads and provide recommendations for improvement."
        ),
        Goal(
            priority=4,
            name="Terminate",
            description="Provide a comprehensive architecture assessment with recommendations for scalability and system design improvements."
        )
    ]

    action_registry = PythonActionRegistry(tags=["fintech", "architecture", "file_operations", "system"])

    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )

def create_comprehensive_fintech_agent() -> Agent:
    """
    Create a comprehensive agent that showcases all FinTech capabilities.
    Uses pattern-based analysis for consistent baseline assessment.
    """
    goals = [
        Goal(
            priority=1,
            name="Comprehensive FinTech Analysis",
            description="Perform a complete analysis covering risk management, performance optimization, regulatory compliance, and system architecture using pattern-based detection."
        ),
        Goal(
            priority=2,
            name="Cross-Domain Integration",
            description="Integrate findings across all analysis domains to provide strategic insights and recommendations."
        ),
        Goal(
            priority=3,
            name="Strategic Assessment",
            description="Provide strategic recommendations for system improvements and enterprise deployment considerations."
        ),
        Goal(
            priority=4,
            name="Terminate",
            description="Provide a comprehensive analysis report that demonstrates deep technical understanding across all FinTech domains."
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