"""
Unit tests for FinTech specialized agents.

Tests agent creation, configuration, and goal structures for all
FinTech pattern-based analysis agents.
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.agents.file_explorer.fintech_agents import (
    create_risk_management_agent,
    create_performance_agent,
    create_compliance_agent,
    create_architecture_agent,
    create_comprehensive_fintech_agent
)


class TestFinTechAgentCreation:
    """Test that all FinTech agents can be created successfully."""
    
    def test_create_risk_management_agent(self):
        """Test risk management agent creation."""
        agent = create_risk_management_agent()
        
        assert agent is not None
        assert len(agent.goals) == 4
        assert any("risk" in goal.name.lower() for goal in agent.goals)
        assert any("terminate" in goal.name.lower() for goal in agent.goals)
        
        # Test that agent has access to risk management tools
        actions = agent.actions.get_actions()
        action_names = [action.name for action in actions]
        assert "analyze_financial_risk_patterns" in action_names
        assert "terminate" in action_names
    
    def test_create_performance_agent(self):
        """Test performance optimization agent creation."""
        agent = create_performance_agent()
        
        assert agent is not None
        assert len(agent.goals) == 4
        assert any("performance" in goal.name.lower() for goal in agent.goals)
        
        # Test that agent has access to performance tools
        actions = agent.actions.get_actions()
        action_names = [action.name for action in actions]
        assert "analyze_hft_performance_patterns" in action_names
    
    def test_create_compliance_agent(self):
        """Test compliance and security agent creation."""
        agent = create_compliance_agent()
        
        assert agent is not None
        assert len(agent.goals) == 4
        assert any("compliance" in goal.name.lower() or "security" in goal.name.lower() 
                  for goal in agent.goals)
        
        # Test that agent has access to compliance tools
        actions = agent.actions.get_actions()
        action_names = [action.name for action in actions]
        assert "analyze_regulatory_compliance" in action_names
    
    def test_create_architecture_agent(self):
        """Test FinTech architecture agent creation."""
        agent = create_architecture_agent()
        
        assert agent is not None
        assert len(agent.goals) == 4
        assert any("architecture" in goal.name.lower() for goal in agent.goals)
        
        # Test that agent has access to architecture tools
        actions = agent.actions.get_actions()
        action_names = [action.name for action in actions]
        assert "analyze_fintech_architecture_patterns" in action_names
    
    def test_create_comprehensive_fintech_agent(self):
        """Test comprehensive FinTech agent creation."""
        agent = create_comprehensive_fintech_agent()
        
        assert agent is not None
        assert len(agent.goals) == 4
        assert any("comprehensive" in goal.name.lower() for goal in agent.goals)
        
        # Test that agent has access to ALL FinTech tools
        actions = agent.actions.get_actions()
        action_names = [action.name for action in actions]
        
        expected_tools = [
            "analyze_financial_risk_patterns",
            "analyze_hft_performance_patterns", 
            "analyze_regulatory_compliance",
            "analyze_fintech_architecture_patterns",
            "analyze_fintech_project_comprehensive"
        ]
        
        for tool in expected_tools:
            assert tool in action_names, f"Missing tool: {tool}"


class TestFinTechAgentGoals:
    """Test goal structures and priorities for FinTech agents."""
    
    def test_risk_management_goals(self):
        """Test risk management agent goal structure."""
        agent = create_risk_management_agent()
        
        goal_names = [goal.name for goal in agent.goals]
        goal_descriptions = [goal.description for goal in agent.goals]
        
        # Check for risk-specific goals
        assert any("risk" in name.lower() for name in goal_names)
        assert any("pattern" in desc.lower() for desc in goal_descriptions)
        assert any("control" in desc.lower() for desc in goal_descriptions)
        
        # Check goal priorities are set
        priorities = [goal.priority for goal in agent.goals]
        assert len(set(priorities)) == len(priorities)  # All unique priorities
        assert min(priorities) == 1  # Starts at 1
        assert max(priorities) <= 4  # No more than 4 goals
    
    def test_performance_goals(self):
        """Test performance agent goal structure."""
        agent = create_performance_agent()
        
        goal_descriptions = [goal.description for goal in agent.goals]
        
        # Check for performance-specific goals
        assert any("performance" in desc.lower() for desc in goal_descriptions)
        assert any("optimization" in desc.lower() for desc in goal_descriptions)
        assert any("trading" in desc.lower() for desc in goal_descriptions)
    
    def test_compliance_goals(self):
        """Test compliance agent goal structure."""
        agent = create_compliance_agent()
        
        goal_descriptions = [goal.description for goal in agent.goals]
        
        # Check for compliance-specific goals
        assert any("security" in desc.lower() for desc in goal_descriptions)
        assert any("compliance" in desc.lower() for desc in goal_descriptions)
        assert any("regulatory" in desc.lower() for desc in goal_descriptions)


class TestFinTechAgentConfiguration:
    """Test agent configuration and tool access."""
    
    def test_agent_tool_filtering(self):
        """Test that agents get appropriate tool sets."""
        risk_agent = create_risk_management_agent()
        performance_agent = create_performance_agent()
        
        risk_actions = [action.name for action in risk_agent.actions.get_actions()]
        perf_actions = [action.name for action in performance_agent.actions.get_actions()]
        
        # Both should have basic file operations
        assert "read_project_file" in risk_actions
        assert "read_project_file" in perf_actions
        
        # Both should have their specialized tools
        assert "analyze_financial_risk_patterns" in risk_actions
        assert "analyze_hft_performance_patterns" in perf_actions
    
    def test_comprehensive_agent_tools(self):
        """Test that comprehensive agent has access to all tools."""
        agent = create_comprehensive_fintech_agent()
        actions = [action.name for action in agent.actions.get_actions()]
        
        # Should have ALL FinTech analysis tools
        fintech_tools = [
            "analyze_financial_risk_patterns",
            "analyze_hft_performance_patterns",
            "analyze_regulatory_compliance", 
            "analyze_fintech_architecture_patterns",
            "analyze_fintech_project_comprehensive"
        ]
        
        for tool in fintech_tools:
            assert tool in actions
        
        # Should also have basic file operations
        basic_tools = ["read_project_file", "list_project_files", "terminate"]
        for tool in basic_tools:
            assert tool in actions
    
    def test_agent_environment_setup(self):
        """Test that agents have proper environment configuration."""
        agent = create_risk_management_agent()
        
        assert agent.environment is not None
        assert agent.agent_language is not None
        assert agent.generate_response is not None
        assert hasattr(agent, 'goals')
        assert hasattr(agent, 'actions')


class TestFinTechAgentErrorHandling:
    """Test error handling and edge cases."""
    
    def test_agent_creation_resilience(self):
        """Test that agent creation handles various conditions."""
        # Test multiple creations don't interfere
        agent1 = create_risk_management_agent()
        agent2 = create_risk_management_agent()
        
        assert agent1 is not agent2  # Different instances
        assert len(agent1.goals) == len(agent2.goals)  # Same configuration
    
    def test_agent_action_registry_independence(self):
        """Test that different agents have independent registries."""
        risk_agent = create_risk_management_agent()
        compliance_agent = create_compliance_agent()
        
        risk_actions = set(action.name for action in risk_agent.actions.get_actions())
        compliance_actions = set(action.name for action in compliance_agent.actions.get_actions())
        
        # Should have different specialized tools
        assert "analyze_financial_risk_patterns" in risk_actions
        assert "analyze_regulatory_compliance" in compliance_actions
        
        # Both should have common tools
        common_tools = risk_actions & compliance_actions
        assert "read_project_file" in common_tools
        assert "terminate" in common_tools


if __name__ == "__main__":
    pytest.main([__file__, "-v"])