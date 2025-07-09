"""
Unit tests for the Agent Registry system.

Tests agent discovery, selection, categorization, and utility functions
that enable dynamic agent management.
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.agents.file_explorer.agent_registry import (
    get_available_agents,
    get_agents_by_category,
    create_agent_for_use_case,
    get_analysis_mode_info,
    get_recommended_agent,
    list_available_agents,
    create_agent_by_key
)


class TestAgentDiscovery:
    """Test agent discovery and listing functionality."""
    
    def test_get_available_agents(self):
        """Test that all agents can be discovered."""
        agents = get_available_agents()
        
        assert isinstance(agents, dict)
        assert len(agents) >= 12, "Should have at least 12 agents"
        
        # Check expected agent keys exist
        expected_agents = [
            "risk_management", "performance", "compliance", "architecture", "comprehensive",
            "hybrid_risk", "hybrid_compliance", "hybrid_performance", "hybrid_comprehensive", 
            "file_explorer", "readme", "code_analysis"
        ]
        
        for agent_key in expected_agents:
            assert agent_key in agents, f"Missing agent: {agent_key}"
    
    def test_agent_metadata_structure(self):
        """Test that agent metadata has correct structure."""
        agents = get_available_agents()
        
        for agent_key, agent_info in agents.items():
            # Required fields
            required_fields = ["name", "description", "factory", "use_case", "analysis_type", "category"]
            for field in required_fields:
                assert field in agent_info, f"Agent {agent_key} missing field: {field}"
            
            # Validate field types
            assert isinstance(agent_info["name"], str)
            assert isinstance(agent_info["description"], str)
            assert callable(agent_info["factory"])
            assert isinstance(agent_info["use_case"], str)
            assert isinstance(agent_info["analysis_type"], str)
            assert isinstance(agent_info["category"], str)
    
    def test_get_agents_by_category(self):
        """Test agent categorization."""
        categories = get_agents_by_category()
        
        assert isinstance(categories, dict)
        
        # Expected categories
        expected_categories = ["FinTech Specialized", "Hybrid Analysis", "Basic Utilities"]
        for category in expected_categories:
            assert category in categories, f"Missing category: {category}"
        
        # Check category contents
        fintech_agents = categories["FinTech Specialized"]
        assert len(fintech_agents) == 5, "Should have 5 FinTech specialized agents"
        
        hybrid_agents = categories["Hybrid Analysis"]
        assert len(hybrid_agents) == 4, "Should have 4 hybrid analysis agents"
        
        basic_agents = categories["Basic Utilities"]
        assert len(basic_agents) == 3, "Should have 3 basic utility agents"


class TestAgentCreation:
    """Test agent creation functionality."""
    
    def test_create_agent_by_key(self):
        """Test creating agents by registry key."""
        # Test creating different types of agents
        agent_keys = ["risk_management", "hybrid_compliance", "file_explorer"]
        
        for key in agent_keys:
            agent = create_agent_by_key(key)
            assert agent is not None, f"Failed to create agent: {key}"
            assert hasattr(agent, 'goals')
            assert hasattr(agent, 'actions') 
            assert len(agent.goals) > 0
    
    def test_create_agent_by_invalid_key(self):
        """Test error handling for invalid agent keys."""
        with pytest.raises(KeyError):
            create_agent_by_key("nonexistent_agent")
    
    def test_create_agent_for_use_case(self):
        """Test creating agents for specific use cases."""
        use_cases = {
            "trading_systems": "pattern",
            "compliance_review": "pattern", 
            "architecture_review": "pattern",
            "technical_assessment": "pattern"
        }
        
        for use_case, mode in use_cases.items():
            agent = create_agent_for_use_case(use_case, mode)
            assert agent is not None, f"Failed to create agent for use case: {use_case}"
            assert len(agent.goals) > 0
    
    def test_create_agent_for_hybrid_use_case(self):
        """Test creating hybrid agents for use cases."""
        use_cases = ["trading_systems", "compliance_review", "technical_assessment"]
        
        for use_case in use_cases:
            agent = create_agent_for_use_case(use_case, "hybrid")
            assert agent is not None, f"Failed to create hybrid agent for: {use_case}"
            
            # Hybrid agents should have same or more sophisticated goals
            assert len(agent.goals) >= 3


class TestAnalysisModes:
    """Test analysis mode information and configuration."""
    
    def test_get_analysis_mode_info(self):
        """Test analysis mode information structure."""
        modes = get_analysis_mode_info()
        
        assert isinstance(modes, dict)
        
        # Expected modes
        expected_modes = ["pattern", "hybrid", "basic"]
        for mode in expected_modes:
            assert mode in modes, f"Missing analysis mode: {mode}"
        
        # Check mode structure
        for mode_key, mode_info in modes.items():
            required_fields = ["name", "description", "benefits", "use_cases", "agents"]
            for field in required_fields:
                assert field in mode_info, f"Mode {mode_key} missing field: {field}"
            
            assert isinstance(mode_info["benefits"], list)
            assert isinstance(mode_info["use_cases"], list)
            assert isinstance(mode_info["agents"], list)
            assert len(mode_info["benefits"]) > 0
            assert len(mode_info["use_cases"]) > 0
            assert len(mode_info["agents"]) > 0
    
    def test_analysis_mode_agent_mapping(self):
        """Test that analysis modes correctly map to available agents."""
        modes = get_analysis_mode_info()
        available_agents = get_available_agents()
        
        for mode_key, mode_info in modes.items():
            mode_agents = mode_info["agents"]
            
            # All listed agents should exist
            for agent_key in mode_agents:
                assert agent_key in available_agents, \
                       f"Mode {mode_key} references non-existent agent: {agent_key}"


class TestAgentRecommendations:
    """Test agent recommendation system."""
    
    def test_get_recommended_agent_fintech(self):
        """Test recommendations for FinTech domain."""
        requirements = {
            "domain": "fintech",
            "complexity": "comprehensive",
            "speed_priority": False,
            "depth_priority": True
        }
        
        recommended = get_recommended_agent(requirements)
        assert recommended in ["hybrid_comprehensive", "comprehensive"]
    
    def test_get_recommended_agent_basic(self):
        """Test recommendations for basic use cases."""
        requirements = {
            "domain": "general",
            "complexity": "basic",
            "speed_priority": True,
            "depth_priority": False
        }
        
        recommended = get_recommended_agent(requirements)
        assert recommended in ["file_explorer", "code_analysis"]
    
    def test_get_recommended_agent_documentation(self):
        """Test recommendations for documentation focus."""
        requirements = {
            "domain": "documentation",
            "complexity": "basic"
        }
        
        recommended = get_recommended_agent(requirements)
        assert recommended == "readme"
    
    def test_recommendation_edge_cases(self):
        """Test recommendation system with edge cases."""
        # Empty requirements
        recommended = get_recommended_agent({})
        assert recommended in get_available_agents()
        
        # Conflicting requirements
        requirements = {
            "domain": "fintech",
            "complexity": "basic",
            "speed_priority": True,
            "depth_priority": True  # Conflicting with speed
        }
        recommended = get_recommended_agent(requirements)
        assert recommended in get_available_agents()


class TestAgentRegistryUtilities:
    """Test utility functions for agent management."""
    
    def test_list_available_agents_output(self):
        """Test that list_available_agents produces output."""
        import io
        import sys
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            list_available_agents()
            output = captured_output.getvalue()
            
            # Should produce substantial output
            assert len(output) > 100, "Should produce detailed agent listing"
            
            # Should mention key categories
            assert "FinTech Specialized" in output
            assert "Hybrid Analysis" in output
            assert "Basic Utilities" in output
            
        finally:
            sys.stdout = sys.__stdout__
    
    def test_agent_factory_functions_work(self):
        """Test that all agent factory functions in registry work."""
        agents = get_available_agents()
        
        # Test a sample of different agent types
        test_agents = ["risk_management", "hybrid_compliance", "file_explorer", "comprehensive"]
        
        for agent_key in test_agents:
            assert agent_key in agents
            factory = agents[agent_key]["factory"]
            
            # Factory should be callable and return an agent
            assert callable(factory)
            agent = factory()
            assert agent is not None
            assert hasattr(agent, 'goals')
            assert hasattr(agent, 'actions')


class TestRegistryConsistency:
    """Test consistency across registry functions."""
    
    def test_agent_count_consistency(self):
        """Test that agent counts are consistent across functions."""
        all_agents = get_available_agents()
        categorized_agents = get_agents_by_category()
        
        # Count agents in categories
        total_categorized = sum(len(agents) for agents in categorized_agents.values())
        
        assert len(all_agents) == total_categorized, \
               "Agent count should be consistent between functions"
    
    def test_agent_key_consistency(self):
        """Test that agent keys are consistent across functions."""
        all_agents = get_available_agents()
        categorized_agents = get_agents_by_category()
        
        # Collect all agent keys from categories
        categorized_keys = set()
        for category_agents in categorized_agents.values():
            categorized_keys.update(category_agents.keys())
        
        all_agent_keys = set(all_agents.keys())
        
        assert all_agent_keys == categorized_keys, \
               "Agent keys should be consistent across functions"
    
    def test_analysis_type_consistency(self):
        """Test that analysis types are consistent."""
        agents = get_available_agents()
        modes = get_analysis_mode_info()
        
        # Extract analysis types from agents
        agent_analysis_types = set(agent["analysis_type"] for agent in agents.values())
        
        # Should have expected analysis types
        expected_types = {"Pattern-Based", "Hybrid (Pattern + AI-Powered)", "Basic"}
        assert agent_analysis_types <= expected_types, \
               "All analysis types should be recognized"


class TestRegistryPerformance:
    """Test performance characteristics of registry functions."""
    
    def test_registry_function_speed(self):
        """Test that registry functions execute quickly."""
        import time
        
        # Test major registry functions
        functions = [
            get_available_agents,
            get_agents_by_category,
            get_analysis_mode_info
        ]
        
        for func in functions:
            start_time = time.time()
            result = func()
            execution_time = time.time() - start_time
            
            assert execution_time < 0.1, f"{func.__name__} should execute quickly"
            assert result is not None and len(result) > 0
    
    def test_agent_creation_caching(self):
        """Test that repeated agent creation works consistently."""
        agent_key = "risk_management"
        
        # Create the same agent multiple times
        agents = [create_agent_by_key(agent_key) for _ in range(3)]
        
        # Should create different instances
        agent_ids = [id(agent) for agent in agents]
        assert len(set(agent_ids)) == len(agents), "Should create different instances"
        
        # But with same configuration
        goal_counts = [len(agent.goals) for agent in agents]
        assert len(set(goal_counts)) == 1, "Should have consistent configuration"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])