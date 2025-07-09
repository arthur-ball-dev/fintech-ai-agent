"""
Unit tests for Hybrid Analysis agents.

Tests agents that combine pattern-based detection with AI-powered 
contextual analysis for maximum insight depth.
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.agents.file_explorer.hybrid_agents import (
    create_hybrid_risk_management_agent,
    create_hybrid_compliance_agent,
    create_hybrid_performance_agent,
    create_hybrid_comprehensive_agent
)


class TestHybridAgentCreation:
    """Test that all hybrid agents can be created successfully."""
    
    def test_create_hybrid_risk_management_agent(self):
        """Test hybrid risk management agent creation."""
        agent = create_hybrid_risk_management_agent()
        
        assert agent is not None
        assert len(agent.goals) == 4
        assert any("hybrid" in goal.name.lower() or "risk" in goal.name.lower() 
                  for goal in agent.goals)
        
        # Test that agent has access to risk management tools
        actions = agent.actions.get_actions()
        action_names = [action.name for action in actions]
        assert "analyze_financial_risk_patterns" in action_names
        assert "terminate" in action_names
    
    def test_create_hybrid_compliance_agent(self):
        """Test hybrid compliance agent creation."""
        agent = create_hybrid_compliance_agent()
        
        assert agent is not None
        assert len(agent.goals) == 4
        assert any("compliance" in goal.name.lower() or "hybrid" in goal.name.lower()
                  for goal in agent.goals)
        
        # Test that agent has access to compliance tools
        actions = agent.actions.get_actions()
        action_names = [action.name for action in actions]
        assert "analyze_regulatory_compliance" in action_names
    
    def test_create_hybrid_performance_agent(self):
        """Test hybrid performance agent creation."""
        agent = create_hybrid_performance_agent()
        
        assert agent is not None
        assert len(agent.goals) == 4
        assert any("performance" in goal.name.lower() or "hybrid" in goal.name.lower()
                  for goal in agent.goals)
        
        # Test that agent has access to performance tools
        actions = agent.actions.get_actions()
        action_names = [action.name for action in actions]
        assert "analyze_hft_performance_patterns" in action_names
    
    def test_create_hybrid_comprehensive_agent(self):
        """Test hybrid comprehensive agent creation."""
        agent = create_hybrid_comprehensive_agent()
        
        assert agent is not None
        assert len(agent.goals) == 4
        assert any("comprehensive" in goal.name.lower() or "hybrid" in goal.name.lower()
                  for goal in agent.goals)
        
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


class TestHybridAgentGoals:
    """Test goal structures specific to hybrid analysis."""
    
    def test_hybrid_goals_mention_ai_analysis(self):
        """Test that hybrid agent goals reference AI-powered analysis."""
        agents = [
            create_hybrid_risk_management_agent(),
            create_hybrid_compliance_agent(),
            create_hybrid_performance_agent(),
            create_hybrid_comprehensive_agent()
        ]
        
        for agent in agents:
            goal_descriptions = [goal.description.lower() for goal in agent.goals]
            
            # At least one goal should mention hybrid, AI, or contextual analysis
            hybrid_keywords = ["hybrid", "ai", "contextual", "insights", "business"]
            assert any(any(keyword in desc for keyword in hybrid_keywords) 
                      for desc in goal_descriptions), \
                   "Hybrid agent should have AI-focused goals"
    
    def test_hybrid_vs_pattern_goal_differences(self):
        """Test that hybrid agents have different goals than pattern-based agents."""
        from src.agents.file_explorer.fintech_agents import create_risk_management_agent
        
        pattern_agent = create_risk_management_agent()
        hybrid_agent = create_hybrid_risk_management_agent()
        
        pattern_goals = [goal.description for goal in pattern_agent.goals]
        hybrid_goals = [goal.description for goal in hybrid_agent.goals]
        
        # Should have different goal descriptions
        assert pattern_goals != hybrid_goals
        
        # Hybrid goals should mention additional analysis
        hybrid_text = " ".join(hybrid_goals).lower()
        assert any(keyword in hybrid_text for keyword in 
                  ["contextual", "insights", "business", "ai", "integrated"])


class TestHybridAgentCapabilities:
    """Test capabilities unique to hybrid agents."""
    
    def test_hybrid_agents_have_same_tools_as_pattern_agents(self):
        """Test that hybrid agents have access to same tools as pattern agents."""
        from src.agents.file_explorer.fintech_agents import (
            create_risk_management_agent,
            create_compliance_agent
        )
        
        # Compare tools between pattern and hybrid agents
        pattern_risk = create_risk_management_agent()
        hybrid_risk = create_hybrid_risk_management_agent()
        
        pattern_tools = set(action.name for action in pattern_risk.actions.get_actions())
        hybrid_tools = set(action.name for action in hybrid_risk.actions.get_actions())
        
        # Hybrid agents should have all the same tools as pattern agents
        assert pattern_tools == hybrid_tools, \
               "Hybrid agents should have same tool access as pattern agents"
    
    def test_comprehensive_hybrid_tool_access(self):
        """Test that comprehensive hybrid agent has maximum tool access."""
        agent = create_hybrid_comprehensive_agent()
        actions = [action.name for action in agent.actions.get_actions()]
        
        # Should have comprehensive tag access
        expected_categories = [
            "file_operations",  # Basic file tools
            "fintech",         # All FinTech analysis tools
            "system"           # System operations like terminate
        ]
        
        # Verify comprehensive tool access by checking for tools from each category
        assert "read_project_file" in actions  # file_operations
        assert "analyze_fintech_project_comprehensive" in actions  # fintech
        assert "terminate" in actions  # system


class TestHybridAgentDocumentation:
    """Test that hybrid agents are properly documented."""
    
    def test_agent_docstrings_mention_hybrid_analysis(self):
        """Test that hybrid agent factory functions have proper documentation."""
        import inspect
        
        functions = [
            create_hybrid_risk_management_agent,
            create_hybrid_compliance_agent, 
            create_hybrid_performance_agent,
            create_hybrid_comprehensive_agent
        ]
        
        for func in functions:
            docstring = inspect.getdoc(func)
            assert docstring is not None, f"{func.__name__} missing docstring"
            
            docstring_lower = docstring.lower()
            hybrid_keywords = ["hybrid", "pattern", "ai", "contextual", "combines"]
            assert any(keyword in docstring_lower for keyword in hybrid_keywords), \
                   f"{func.__name__} docstring should describe hybrid analysis"
    
    def test_agent_goals_are_descriptive(self):
        """Test that agent goals have descriptive names and descriptions."""
        agent = create_hybrid_comprehensive_agent()
        
        for goal in agent.goals:
            # Goals should have meaningful names
            assert len(goal.name) > 5, "Goal names should be descriptive"
            assert len(goal.description) > 20, "Goal descriptions should be detailed"
            
            # Priority should be reasonable
            assert 1 <= goal.priority <= 10, "Goal priority should be reasonable"


class TestHybridAgentIntegration:
    """Test integration aspects of hybrid agents."""
    
    def test_hybrid_agents_use_same_framework(self):
        """Test that hybrid agents use the same framework components."""
        agent = create_hybrid_risk_management_agent()
        
        # Should use standard framework components
        assert hasattr(agent, 'goals')
        assert hasattr(agent, 'actions')
        assert hasattr(agent, 'environment')
        assert hasattr(agent, 'agent_language')
        assert hasattr(agent, 'generate_response')
        
        # Components should not be None
        assert agent.goals is not None
        assert agent.actions is not None
        assert agent.environment is not None
    
    def test_hybrid_agent_action_registry_filtering(self):
        """Test that hybrid agents properly filter actions by tags."""
        risk_agent = create_hybrid_risk_management_agent()
        compliance_agent = create_hybrid_compliance_agent()
        
        risk_actions = set(action.name for action in risk_agent.actions.get_actions())
        compliance_actions = set(action.name for action in compliance_agent.actions.get_actions())
        
        # Should have core FinTech tools
        assert "analyze_financial_risk_patterns" in risk_actions
        assert "analyze_regulatory_compliance" in compliance_actions
        
        # Should have common file operations
        common_tools = risk_actions & compliance_actions
        assert len(common_tools) >= 5, "Should have several common tools"
    
    def test_all_hybrid_agents_can_terminate(self):
        """Test that all hybrid agents have termination capability."""
        agents = [
            create_hybrid_risk_management_agent(),
            create_hybrid_compliance_agent(),
            create_hybrid_performance_agent(), 
            create_hybrid_comprehensive_agent()
        ]
        
        for agent in agents:
            actions = [action.name for action in agent.actions.get_actions()]
            assert "terminate" in actions, "All agents should be able to terminate"
            
            # Check that terminate is marked as terminal
            terminate_action = next(action for action in agent.actions.get_actions() 
                                  if action.name == "terminate")
            assert terminate_action.terminal == True, "Terminate action should be terminal"


class TestHybridAgentPerformance:
    """Test performance characteristics of hybrid agents."""
    
    def test_agent_creation_speed(self):
        """Test that hybrid agents can be created quickly."""
        import time
        
        start_time = time.time()
        agent = create_hybrid_comprehensive_agent()
        creation_time = time.time() - start_time
        
        # Agent creation should be fast (under 1 second)
        assert creation_time < 1.0, "Agent creation should be fast"
        assert agent is not None
    
    def test_multiple_agent_creation(self):
        """Test creating multiple hybrid agents."""
        agents = []
        
        # Create multiple agents of different types
        for _ in range(3):
            agents.extend([
                create_hybrid_risk_management_agent(),
                create_hybrid_compliance_agent()
            ])
        
        # All agents should be different instances
        agent_ids = [id(agent) for agent in agents]
        assert len(set(agent_ids)) == len(agents), "Each agent should be unique instance"
        
        # All should be properly configured
        for agent in agents:
            assert len(agent.goals) > 0
            assert len(agent.actions.get_actions()) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])