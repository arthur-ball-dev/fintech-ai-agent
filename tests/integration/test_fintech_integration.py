"""
Integration tests for FinTech analysis workflows.

Tests complete agent execution, tool integration, and analysis
capabilities without requiring live LLM API calls.
"""
import pytest
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.agents.file_explorer import (
    create_risk_management_agent,
    create_hybrid_compliance_agent,
    create_comprehensive_fintech_agent,
    create_agent_by_key
)
from src.agents.file_explorer.actions import (
    analyze_financial_risk_patterns,
    analyze_regulatory_compliance,
    analyze_hft_performance_patterns,
    analyze_fintech_architecture_patterns
)


class TestFinTechAnalysisTools:
    """Test FinTech analysis tools with sample code."""
    
    def setup_method(self):
        """Set up test environment with sample code files."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create sample Python files with FinTech patterns
        self.create_sample_files()
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_sample_files(self):
        """Create sample files with various FinTech patterns."""
        
        # Risk management file
        risk_file = """
import logging
from datetime import datetime

MAX_POSITION = 10000
POSITION_LIMIT = 50000

def check_position_limit(position_size):
    if position_size > MAX_POSITION:
        return False
    return True

def calculate_stop_loss(entry_price, risk_per_trade=0.02):
    return entry_price * (1 - risk_per_trade)

def audit_trail(user_id, action, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow()
    logging.info(f"User {user_id}: {action} at {timestamp}")
"""
        
        # Performance optimization file
        performance_file = """
import asyncio
import numpy as np
from collections import deque
import time

async def process_market_data(data):
    # Async processing for low latency
    return await asyncio.sleep(0.001)

class FastQueue:
    __slots__ = ['_queue', '_maxsize']
    
    def __init__(self, maxsize=1000):
        self._queue = deque(maxlen=maxsize)
        self._maxsize = maxsize

def optimize_calculations():
    # Using numpy for performance
    prices = np.array([100.0, 101.0, 99.5, 102.0])
    return np.mean(prices)

# Performance anti-pattern (should be flagged)
def slow_operation():
    time.sleep(0.1)  # This will be flagged
"""
        
        # Compliance/security file
        compliance_file = """
import bcrypt
import ssl
import logging
from datetime import datetime

def encrypt_user_data(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def setup_ssl_context():
    context = ssl.create_default_context()
    return context

def log_compliance_event(user_id, event_type):
    timestamp = datetime.utcnow()
    logging.info(f"COMPLIANCE: {event_type} by user {user_id} at {timestamp}")

# Security risk (should be flagged)
API_KEY = "hardcoded-secret-key"  # This will be flagged
"""
        
        # Architecture file
        architecture_file = """
from fastapi import FastAPI
import redis
import asyncio

app = FastAPI()

# Redis for caching
cache = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/trading/positions")
async def get_positions():
    # API endpoint for trading positions
    return {"positions": []}

class DatabasePool:
    def __init__(self, pool_size=10):
        self.pool_size = pool_size
        
async def queue_processor():
    # Async queue processing
    pass
"""
        
        # Write files
        files = {
            "risk_management.py": risk_file,
            "performance_optimizer.py": performance_file,
            "compliance_module.py": compliance_file, 
            "trading_api.py": architecture_file
        }
        
        for filename, content in files.items():
            with open(filename, 'w') as f:
                f.write(content)
    
    def test_risk_management_analysis(self):
        """Test risk management pattern analysis."""
        result = analyze_financial_risk_patterns(".", include_llm_analysis=False)
        
        assert isinstance(result, str)
        assert "FINANCIAL RISK MANAGEMENT ANALYSIS" in result
        assert "position_limits" in result.lower() or "position" in result.lower()
        assert "risk controls score" in result.lower()
        
        # Should detect the patterns we included
        assert "position_limit" in result.lower() or "max_position" in result.lower()
        assert "stop_loss" in result.lower() or "risk_per_trade" in result.lower()
    
    def test_performance_analysis(self):
        """Test performance optimization analysis."""
        result = analyze_hft_performance_patterns(".", include_llm_analysis=False)
        
        assert isinstance(result, str)
        assert "HIGH-FREQUENCY TRADING PERFORMANCE ANALYSIS" in result
        assert "performance score" in result.lower()
        
        # Should detect async patterns
        assert "asyncio" in result.lower() or "async" in result.lower()
        # Should detect numpy usage
        assert "numpy" in result.lower()
        # Should flag performance issues
        assert "sleep" in result.lower() or "blocking" in result.lower()
    
    def test_compliance_analysis(self):
        """Test regulatory compliance analysis.""" 
        result = analyze_regulatory_compliance(".", include_llm_analysis=False)
        
        assert isinstance(result, str)
        assert "REGULATORY COMPLIANCE & SECURITY ANALYSIS" in result
        assert "compliance score" in result.lower()
        
        # Should detect security patterns
        assert "bcrypt" in result.lower() or "encrypt" in result.lower()
        assert "ssl" in result.lower()
        
        # Should flag security risks
        assert "hardcoded" in result.lower() or "secret" in result.lower()
    
    def test_architecture_analysis(self):
        """Test architecture pattern analysis."""
        result = analyze_fintech_architecture_patterns(".", include_llm_analysis=False)
        
        assert isinstance(result, str)
        assert "FINTECH ARCHITECTURE ANALYSIS" in result
        assert "architecture maturity" in result.lower()
        
        # Should detect FastAPI
        assert "fastapi" in result.lower()
        # Should detect Redis caching
        assert "redis" in result.lower() or "cache" in result.lower()
        # Should detect API endpoints
        assert "api endpoints" in result.lower()


class TestAgentExecution:
    """Test agent execution with mocked LLM responses."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create a simple test file
        with open("test_file.py", "w") as f:
            f.write("# Simple test file\nprint('Hello, FinTech!')\n")
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def mock_llm_response(self, prompt):
        """Mock LLM response based on the context."""
        # Simple mock that returns appropriate tool calls
        if "analyze" in str(prompt).lower():
            return '{"tool": "analyze_financial_risk_patterns", "args": {"project_path": "."}}'
        elif "terminate" in str(prompt).lower():
            return '{"tool": "terminate", "args": {"message": "Analysis complete"}}'
        else:
            return '{"tool": "read_project_file", "args": {"name": "test_file.py"}}'
    
    @patch('src.framework.llm.client.generate_response')
    def test_risk_management_agent_execution(self, mock_generate):
        """Test risk management agent execution flow."""
        mock_generate.side_effect = self.mock_llm_response
        
        agent = create_risk_management_agent()
        
        # Test agent execution with limited iterations
        memory = agent.run("Analyze risk patterns in this project", max_iterations=3)
        
        assert memory is not None
        memories = memory.get_memories()
        assert len(memories) > 0
        
        # Should have initial task memory
        assert any("risk" in str(memory).lower() for memory in memories)
    
    @patch('src.framework.llm.client.generate_response')
    def test_hybrid_agent_execution(self, mock_generate):
        """Test hybrid agent execution."""
        mock_generate.side_effect = self.mock_llm_response
        
        agent = create_hybrid_compliance_agent()
        
        # Test execution
        memory = agent.run("Perform compliance analysis", max_iterations=2)
        
        assert memory is not None
        memories = memory.get_memories()
        assert len(memories) > 0
    
    def test_agent_tool_integration(self):
        """Test that agents have access to expected tools."""
        agents = {
            "risk": create_risk_management_agent(),
            "hybrid_comprehensive": create_agent_by_key("hybrid_comprehensive"),
            "comprehensive": create_comprehensive_fintech_agent()
        }
        
        for agent_type, agent in agents.items():
            actions = [action.name for action in agent.actions.get_actions()]
            
            # All should have basic file operations
            assert "read_project_file" in actions
            assert "terminate" in actions
            
            # Comprehensive agents should have all FinTech tools
            if "comprehensive" in agent_type:
                fintech_tools = [
                    "analyze_financial_risk_patterns",
                    "analyze_regulatory_compliance",
                    "analyze_hft_performance_patterns",
                    "analyze_fintech_architecture_patterns"
                ]
                for tool in fintech_tools:
                    assert tool in actions, f"Missing tool {tool} in {agent_type}"


class TestHybridAnalysisWorkflow:
    """Test hybrid analysis workflows that combine pattern and LLM analysis."""
    
    def setup_method(self):
        """Set up test with sample FinTech code."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create sample file with risk patterns
        sample_code = """
import logging
from datetime import datetime

MAX_POSITION_SIZE = 100000
STOP_LOSS_PERCENTAGE = 0.02

def validate_position(position_size):
    if position_size > MAX_POSITION_SIZE:
        logging.error("Position exceeds limit")
        return False
    return True

def calculate_risk_metrics(portfolio):
    # Calculate VaR and other risk metrics
    pass

# Hardcoded API key (security risk)
API_SECRET = "sk-1234567890abcdef"
"""
        
        with open("trading_system.py", "w") as f:
            f.write(sample_code)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd) 
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_pattern_based_analysis(self):
        """Test pattern-based analysis (no LLM)."""
        result = analyze_financial_risk_patterns(".", include_llm_analysis=False)
        
        # Should detect patterns
        assert "position" in result.lower()
        assert "risk controls score" in result.lower()
        assert "PATTERN-BASED ANALYSIS" in result
        
        # Should not include LLM analysis
        assert "LLM CONTEXTUAL ANALYSIS" not in result
    
    def test_hybrid_analysis_structure(self):
        """Test hybrid analysis structure (pattern + LLM placeholder)."""
        result = analyze_financial_risk_patterns(".", include_llm_analysis=True)
        
        # Should include both pattern and LLM sections
        assert "PATTERN-BASED ANALYSIS" in result
        assert "LLM CONTEXTUAL ANALYSIS" in result or "placeholder" in result.lower()
        assert "INTEGRATED RISK ASSESSMENT" in result
    
    def test_compliance_hybrid_workflow(self):
        """Test compliance analysis with hybrid mode."""
        result = analyze_regulatory_compliance(".", include_llm_analysis=True)
        
        # Should detect the hardcoded secret
        assert "hardcoded" in result.lower() or "secret" in result.lower()
        
        # Should have hybrid analysis structure
        assert "PATTERN-BASED ANALYSIS" in result
        
        # Should mention integration
        assert "INTEGRATED" in result or "integrated" in result.lower()


class TestAgentRegistryIntegration:
    """Test integration of agent registry with actual agent execution."""
    
    def test_registry_agent_creation_integration(self):
        """Test that registry creates working agents."""
        from src.agents.file_explorer.agent_registry import get_available_agents
        
        agents = get_available_agents()
        
        # Test a sample of agents from each category
        test_agents = ["risk_management", "hybrid_compliance", "file_explorer"]
        
        for agent_key in test_agents:
            assert agent_key in agents
            
            # Create agent using registry
            factory = agents[agent_key]["factory"]
            agent = factory()
            
            # Verify agent is properly configured
            assert agent is not None
            assert len(agent.goals) > 0
            assert len(agent.actions.get_actions()) > 0
            
            # Test agent metadata matches capabilities
            agent_info = agents[agent_key]
            if "fintech" in agent_info["category"].lower():
                actions = [action.name for action in agent.actions.get_actions()]
                fintech_actions = [a for a in actions if "fintech" in a or 
                                  any(keyword in a for keyword in ["risk", "compliance", "performance"])]
                assert len(fintech_actions) > 0, f"FinTech agent {agent_key} should have FinTech tools"
    
    def test_use_case_agent_appropriateness(self):
        """Test that use case agents have appropriate tools."""
        from src.agents.file_explorer.agent_registry import create_agent_for_use_case
        
        use_cases = {
            "trading_systems": ["performance", "hft"],
            "compliance_review": ["compliance", "regulatory"],
            "architecture_review": ["architecture", "fintech"]
        }
        
        for use_case, expected_keywords in use_cases.items():
            agent = create_agent_for_use_case(use_case, "pattern")
            actions = [action.name for action in agent.actions.get_actions()]
            
            # Should have tools relevant to the use case
            relevant_tools = [action for action in actions 
                            if any(keyword in action.lower() for keyword in expected_keywords)]
            assert len(relevant_tools) > 0, f"Use case {use_case} should have relevant tools"


class TestCompleteWorkflow:
    """Test complete end-to-end workflows."""
    
    def setup_method(self):
        """Set up comprehensive test environment.""" 
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create a comprehensive FinTech project structure
        self.create_fintech_project()
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_fintech_project(self):
        """Create a realistic FinTech project structure."""
        project_files = {
            "trading_engine.py": """
import asyncio
import logging
from datetime import datetime

MAX_POSITION = 50000
STOP_LOSS_RATIO = 0.02

async def execute_trade(symbol, quantity, price):
    if quantity * price > MAX_POSITION:
        logging.error("Position exceeds limit")
        return False
    return True
""",
            "risk_manager.py": """
import numpy as np
from typing import Dict, List

def calculate_var(positions: List[float], confidence: float = 0.95) -> float:
    return np.percentile(positions, (1 - confidence) * 100)

def check_exposure_limits(portfolio: Dict) -> bool:
    total_exposure = sum(portfolio.values())
    return total_exposure < 1000000
""",
            "compliance.py": """
import bcrypt
import logging
from datetime import datetime

def hash_user_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def audit_log(user_id: str, action: str):
    timestamp = datetime.utcnow()
    logging.info(f"AUDIT: {user_id} performed {action} at {timestamp}")

# Security vulnerability (should be detected)
SECRET_KEY = "hardcoded-secret-123"
""",
            "api_server.py": """
from fastapi import FastAPI
import redis

app = FastAPI()
cache = redis.Redis()

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/positions")
async def get_positions():
    return {"positions": []}
"""
        }
        
        for filename, content in project_files.items():
            with open(filename, 'w') as f:
                f.write(content)
    
    def test_comprehensive_analysis_workflow(self):
        """Test comprehensive FinTech analysis across all domains."""
        # Run comprehensive analysis
        from src.agents.file_explorer.actions import analyze_fintech_project_comprehensive
        
        result = analyze_fintech_project_comprehensive(".", include_llm_analysis=False)
        
        assert isinstance(result, str)
        assert "COMPREHENSIVE FINTECH PROJECT ANALYSIS" in result
        
        # Should include all analysis domains
        assert "FINANCIAL RISK MANAGEMENT ANALYSIS" in result
        assert "HIGH-FREQUENCY TRADING PERFORMANCE ANALYSIS" in result  
        assert "REGULATORY COMPLIANCE & SECURITY ANALYSIS" in result
        assert "FINTECH ARCHITECTURE ANALYSIS" in result
        
        # Should detect patterns from our sample files
        assert "position" in result.lower()
        assert "asyncio" in result.lower() or "async" in result.lower()
        assert "bcrypt" in result.lower() or "hash" in result.lower()
        assert "fastapi" in result.lower()
        assert "hardcoded" in result.lower()  # Security risk


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])