"""
Performance tests for FinTech analysis capabilities.

Tests system performance with large codebases, multiple agents,
and stress testing scenarios typical of enterprise environments.
"""
import pytest
import sys
import tempfile
import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.agents.file_explorer.actions import (
    analyze_financial_risk_patterns,
    analyze_regulatory_compliance,
    analyze_hft_performance_patterns,
    analyze_fintech_architecture_patterns,
    analyze_fintech_project_comprehensive
)
from src.agents.file_explorer import (
    create_comprehensive_fintech_agent,
    create_agent_by_key,
    get_available_agents
)


class TestAnalysisPerformance:
    """Test performance of FinTech analysis tools."""
    
    def setup_method(self):
        """Set up performance test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_large_codebase(self, num_files=50, lines_per_file=100):
        """Create a large codebase for performance testing."""
        
        # Template for different types of files
        templates = {
            "risk": """
import logging
import numpy as np
from datetime import datetime

MAX_POSITION_{i} = {i * 1000}
RISK_LIMIT_{i} = {i * 500}

def check_position_limit_{i}(position):
    if position > MAX_POSITION_{i}:
        logging.error("Position exceeds limit")
        return False
    return True

def calculate_stop_loss_{i}(price, risk_pct=0.02):
    return price * (1 - risk_pct)

def portfolio_var_{i}(positions):
    return np.percentile(positions, 5)

def audit_trail_{i}(user_id, action):
    timestamp = datetime.utcnow()
    logging.info(f"User {{user_id}}: {{action}} at {{timestamp}}")

class RiskManager_{i}:
    def __init__(self):
        self.max_exposure = {i * 10000}
        self.position_limits = {{"equity": {i * 1000}, "fx": {i * 500}}}
    
    def validate_trade(self, symbol, quantity, price):
        total_value = quantity * price
        if total_value > self.max_exposure:
            return False
        return True
""",
            "performance": """
import asyncio
import numpy as np
from collections import deque
import struct
import threading

class FastProcessor_{i}:
    __slots__ = ['_queue', '_buffer', '_size']
    
    def __init__(self, size={i * 100}):
        self._queue = deque(maxlen=size)
        self._buffer = bytearray(size * 8)
        self._size = size

async def process_market_data_{i}(data):
    # High-frequency processing
    processed = np.array(data)
    return np.mean(processed)

def pack_trade_data_{i}(symbol, price, quantity):
    return struct.pack('!f f I', price, quantity, hash(symbol))

async def websocket_handler_{i}():
    # Async websocket processing
    while True:
        await asyncio.sleep(0.001)

def parallel_calculation_{i}():
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(lambda x: x**2, i) for i in range({i})]
        return [f.result() for f in futures]

# Performance anti-pattern (will be detected)
def slow_operation_{i}():
    import time
    time.sleep(0.001)  # This will be flagged
""",
            "compliance": """
import bcrypt
import ssl
import hashlib
import logging
from datetime import datetime

def encrypt_password_{i}(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def setup_ssl_context_{i}():
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    return context

def validate_input_{i}(user_input):
    # Input validation for SQL injection prevention
    dangerous_chars = ["'", '"', ';', '--']
    return not any(char in user_input for char in dangerous_chars)

def log_compliance_event_{i}(user_id, event_type, pii_data=None):
    timestamp = datetime.utcnow()
    if pii_data:
        # Hash PII for GDPR compliance
        hashed_pii = hashlib.sha256(str(pii_data).encode()).hexdigest()
        logging.info(f"COMPLIANCE: {{event_type}} by {{user_id}} at {{timestamp}} - PII: {{hashed_pii}}")
    else:
        logging.info(f"COMPLIANCE: {{event_type}} by {{user_id}} at {{timestamp}}")

# Security vulnerability (will be detected)
API_KEY_{i} = "sk-{i}-hardcoded-secret"
DATABASE_PASSWORD_{i} = "admin123"

class SecurityManager_{i}:
    def __init__(self):
        self.session_timeout = 3600
        self.max_login_attempts = 3
    
    def authenticate_user(self, username, password):
        # Simulate authentication
        return bcrypt.checkpw(password.encode(), b'hashed_password')
""",
            "architecture": """
from fastapi import FastAPI, HTTPException
import redis
import asyncio
from typing import List, Dict

app_{i} = FastAPI(title="Trading API {i}")

# Redis cache for performance
cache_{i} = redis.Redis(host='localhost', port=6379, db={i})

@app_{i}.get("/health/{i}")
async def health_check_{i}():
    return {{"status": "healthy", "service": "trading-api-{i}"}}

@app_{i}.get("/api/v{i}/positions")
async def get_positions_{i}():
    # Cache check
    cached = cache_{i}.get(f"positions_{{i}}")
    if cached:
        return {{"positions": cached, "source": "cache"}}
    
    # Simulate database query
    positions = [{{"symbol": "AAPL", "quantity": {i * 10}}}]
    cache_{i}.setex(f"positions_{{i}}", 300, str(positions))
    return {{"positions": positions, "source": "database"}}

@app_{i}.post("/api/v{i}/orders")
async def create_order_{i}(order: Dict):
    # Rate limiting simulation
    await asyncio.sleep(0.001)
    return {{"order_id": f"ord_{{i}}_{{hash(str(order))}}", "status": "pending"}}

class DatabasePool_{i}:
    def __init__(self, pool_size={i}):
        self.pool_size = pool_size
        self.connections = []
    
    async def get_connection(self):
        # Connection pool management
        return f"connection_{{len(self.connections)}}"

async def message_queue_processor_{i}():
    # Message queue processing
    while True:
        await asyncio.sleep(0.01)

# Microservice configuration
MICROSERVICE_CONFIG_{i} = {{
    "name": f"trading-service-{{i}}",
    "port": 8000 + {i},
    "database_url": f"postgresql://user:pass@localhost/trading_{{i}}",
    "redis_url": f"redis://localhost:6379/{{i}}"
}}
"""
        }
        
        # Create files
        for i in range(num_files):
            template_type = ["risk", "performance", "compliance", "architecture"][i % 4]
            template = templates[template_type]
            
            filename = f"{template_type}_module_{i}.py"
            content = template.format(i=i)
            
            # Add extra lines to reach target line count
            while content.count('\n') < lines_per_file:
                content += f"\n# Additional line {content.count('\n')} for file {i}\n"
            
            with open(filename, 'w') as f:
                f.write(content)
    
    def test_large_codebase_risk_analysis(self):
        """Test risk analysis performance on large codebase."""
        # Create large codebase
        self.create_large_codebase(num_files=100, lines_per_file=50)
        
        start_time = time.time()
        result = analyze_financial_risk_patterns(".", include_llm_analysis=False)
        execution_time = time.time() - start_time
        
        # Should complete within reasonable time (adjust as needed)
        assert execution_time < 10.0, f"Risk analysis took too long: {execution_time:.2f}s"
        assert "FINANCIAL RISK MANAGEMENT ANALYSIS" in result
        assert "Files Analyzed: 100" in result or "100" in result
    
    def test_comprehensive_analysis_performance(self):
        """Test comprehensive analysis performance."""
        # Create medium-sized codebase
        self.create_large_codebase(num_files=50, lines_per_file=30)
        
        start_time = time.time()
        result = analyze_fintech_project_comprehensive(".", include_llm_analysis=False)
        execution_time = time.time() - start_time
        
        # Comprehensive analysis should still be reasonable
        assert execution_time < 15.0, f"Comprehensive analysis took too long: {execution_time:.2f}s"
        assert "COMPREHENSIVE FINTECH PROJECT ANALYSIS" in result
    
    def test_concurrent_analysis_performance(self):
        """Test concurrent analysis of different domains."""
        # Create test codebase
        self.create_large_codebase(num_files=30, lines_per_file=50)
        
        analysis_functions = [
            analyze_financial_risk_patterns,
            analyze_regulatory_compliance,
            analyze_hft_performance_patterns,
            analyze_fintech_architecture_patterns
        ]
        
        # Run analyses concurrently
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(func, ".", False) for func in analysis_functions]
            results = [future.result() for future in futures]
        
        execution_time = time.time() - start_time
        
        # Concurrent execution should be faster than sequential
        assert execution_time < 20.0, f"Concurrent analysis took too long: {execution_time:.2f}s"
        assert len(results) == 4
        assert all(isinstance(result, str) and len(result) > 100 for result in results)
    
    def test_pattern_detection_scalability(self):
        """Test that pattern detection scales linearly."""
        # Test with different codebase sizes
        sizes = [10, 25, 50]
        times = []
        
        for size in sizes:
            # Clean directory
            for file in os.listdir('.'):
                if file.endswith('.py'):
                    os.remove(file)
            
            # Create codebase of specific size
            self.create_large_codebase(num_files=size, lines_per_file=20)
            
            # Measure analysis time
            start_time = time.time()
            analyze_financial_risk_patterns(".", include_llm_analysis=False)
            execution_time = time.time() - start_time
            times.append(execution_time)
        
        # Should scale reasonably (not exponentially)
        # Time for 50 files shouldn't be more than 10x time for 10 files
        assert times[2] < times[0] * 10, "Analysis should scale reasonably with codebase size"
    
    def test_memory_usage_with_large_files(self):
        """Test memory efficiency with large files."""
        import psutil
        import os
        
        # Create few very large files
        large_content = "\n".join([
            f"# Large file line {i}" + 
            f"\ndef function_{i}(): pass" +
            f"\nMAX_VALUE_{i} = {i}"
            for i in range(1000)  # Very large files
        ])
        
        for i in range(5):
            with open(f"large_file_{i}.py", 'w') as f:
                f.write(large_content)
        
        # Measure memory before analysis
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Run analysis
        result = analyze_financial_risk_patterns(".", include_llm_analysis=False)
        
        # Measure memory after analysis
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = memory_after - memory_before
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100, f"Memory usage increased too much: {memory_increase:.1f}MB"
        assert result is not None


class TestAgentPerformance:
    """Test performance of agent creation and execution."""
    
    def test_agent_creation_performance(self):
        """Test that agents can be created quickly."""
        agents_to_test = [
            "risk_management",
            "performance", 
            "compliance",
            "comprehensive",
            "hybrid_comprehensive"
        ]
        
        creation_times = []
        
        for agent_key in agents_to_test:
            start_time = time.time()
            agent = create_agent_by_key(agent_key)
            creation_time = time.time() - start_time
            creation_times.append(creation_time)
            
            # Agent should be created quickly
            assert creation_time < 0.5, f"Agent {agent_key} creation took too long: {creation_time:.3f}s"
            assert agent is not None
            assert len(agent.goals) > 0
    
    def test_concurrent_agent_creation(self):
        """Test creating multiple agents concurrently."""
        agent_keys = ["risk_management", "compliance", "performance"] * 5  # 15 agents
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_agent_by_key, key) for key in agent_keys]
            agents = [future.result() for future in futures]
        
        execution_time = time.time() - start_time
        
        # Should create all agents quickly
        assert execution_time < 3.0, f"Concurrent agent creation took too long: {execution_time:.2f}s"
        assert len(agents) == 15
        assert all(agent is not None for agent in agents)
    
    def test_agent_registry_performance(self):
        """Test performance of agent registry operations."""
        from src.agents.file_explorer.agent_registry import (
            get_available_agents,
            get_agents_by_category,
            get_analysis_mode_info
        )
        
        # Test registry functions performance
        registry_functions = [
            get_available_agents,
            get_agents_by_category, 
            get_analysis_mode_info
        ]
        
        for func in registry_functions:
            start_time = time.time()
            result = func()
            execution_time = time.time() - start_time
            
            assert execution_time < 0.1, f"{func.__name__} took too long: {execution_time:.3f}s"
            assert result is not None
            assert len(result) > 0
    
    def test_tool_registry_performance(self):
        """Test performance of tool discovery and filtering."""
        # Test multiple registry creations (simulates multiple agents)
        from src.framework.actions.registry import PythonActionRegistry
        
        tag_combinations = [
            ["file_operations"],
            ["fintech", "risk_management"],
            ["fintech", "compliance"],
            ["file_operations", "fintech", "system"],
            ["fintech", "comprehensive", "analysis"]
        ]
        
        start_time = time.time()
        
        registries = []
        for tags in tag_combinations * 10:  # 50 registries
            registry = PythonActionRegistry(tags=tags)
            registries.append(registry)
        
        execution_time = time.time() - start_time
        
        # Should create registries quickly
        assert execution_time < 2.0, f"Registry creation took too long: {execution_time:.2f}s"
        assert len(registries) == 50
        assert all(len(registry.get_actions()) > 0 for registry in registries)


class TestStressTests:
    """Stress tests for extreme scenarios."""
    
    def setup_method(self):
        """Set up stress test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_extreme_file_count(self):
        """Test analysis with extreme number of files."""
        # Create many small files
        for i in range(500):  # 500 files
            with open(f"module_{i}.py", 'w') as f:
                f.write(f"""
# Module {i}
import logging

MAX_POSITION_{i} = {i * 100}

def check_limit_{i}(value):
    return value < MAX_POSITION_{i}

def log_action_{i}(action):
    logging.info(f"Action {{action}} in module {i}")
""")
        
        start_time = time.time()
        result = analyze_financial_risk_patterns(".", include_llm_analysis=False)
        execution_time = time.time() - start_time
        
        # Should handle extreme file count
        assert execution_time < 30.0, f"Extreme file count analysis took too long: {execution_time:.2f}s"
        assert "500" in result or "Files Analyzed: 500" in result
    
    def test_files_with_complex_patterns(self):
        """Test analysis with files containing complex pattern combinations."""
        complex_file_content = """
import asyncio
import bcrypt
import logging
import numpy as np
import redis
from datetime import datetime
from fastapi import FastAPI
from collections import deque
import struct
import ssl

# Multiple risk patterns
MAX_POSITION_LIMIT = 1000000
STOP_LOSS_PERCENTAGE = 0.02
PORTFOLIO_VAR_THRESHOLD = 0.05

# Multiple performance patterns  
class FastProcessor:
    __slots__ = ['_queue', '_processor', '_buffer']
    
    def __init__(self):
        self._queue = deque(maxlen=10000)
        self._buffer = bytearray(1024)

async def high_freq_processor():
    while True:
        data = await get_market_data()
        processed = np.array(data)
        await asyncio.sleep(0.0001)

# Multiple compliance patterns
def encrypt_data(data):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(data.encode(), salt)

def audit_transaction(user_id, amount, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow()
    logging.info(f"AUDIT: User {user_id} transaction {amount} at {timestamp}")

# Multiple architecture patterns
app = FastAPI()
cache = redis.Redis()

@app.get("/api/v1/positions")
async def get_positions():
    return {"positions": []}

@app.post("/api/v1/orders")
async def create_order(order_data):
    return {"order_id": "123", "status": "pending"}

# Security vulnerabilities (should be detected)
API_SECRET = "hardcoded-secret-key"
DB_PASSWORD = "admin123"
DEBUG_MODE = True

# Performance anti-patterns (should be detected)
def slow_function():
    import time
    time.sleep(0.1)

def inefficient_loop(items):
    for i in range(len(items)):  # Should use enumerate
        process(items[i])

# More complex patterns
def calculate_portfolio_metrics(positions):
    var_95 = np.percentile(positions, 5)
    var_99 = np.percentile(positions, 1)
    
    if var_95 > PORTFOLIO_VAR_THRESHOLD:
        logging.warning("VaR threshold exceeded")
        return False
    
    return {"var_95": var_95, "var_99": var_99}

async def websocket_handler():
    while True:
        try:
            message = await receive_message()
            await process_message(message)
        except Exception as e:
            logging.error(f"WebSocket error: {e}")

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure = None
    
    def call(self, func, *args, **kwargs):
        if self.failure_count >= self.failure_threshold:
            if datetime.now() - self.last_failure < self.timeout:
                raise Exception("Circuit breaker open")
        
        try:
            result = func(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure = datetime.now()
            raise e
"""
        
        # Create multiple files with complex patterns
        for i in range(20):
            with open(f"complex_module_{i}.py", 'w') as f:
                f.write(complex_file_content.replace("123", str(i)))
        
        start_time = time.time()
        result = analyze_fintech_project_comprehensive(".", include_llm_analysis=False)
        execution_time = time.time() - start_time
        
        # Should handle complex patterns efficiently
        assert execution_time < 10.0, f"Complex pattern analysis took too long: {execution_time:.2f}s"
        
        # Should detect multiple pattern types
        assert "risk" in result.lower()
        assert "performance" in result.lower()
        assert "compliance" in result.lower()
        assert "architecture" in result.lower()
        assert "hardcoded" in result.lower()  # Security risk
    
    def test_repeated_analysis_performance(self):
        """Test performance of repeated analyses (simulates continuous monitoring)."""
        # Create moderate codebase
        for i in range(50):
            with open(f"monitor_module_{i}.py", 'w') as f:
                f.write(f"""
import logging
MAX_POSITION_{i} = {i * 1000}

def check_position_{i}(pos):
    return pos < MAX_POSITION_{i}

def log_trade_{i}(trade_id):
    logging.info(f"Trade {trade_id} in module {i}")
""")
        
        # Run multiple analyses (simulating monitoring)
        times = []
        for iteration in range(5):
            start_time = time.time()
            result = analyze_financial_risk_patterns(".", include_llm_analysis=False)
            execution_time = time.time() - start_time
            times.append(execution_time)
            
            assert result is not None
        
        # Performance should be consistent (no significant degradation)
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        # Variance should be reasonable
        assert max_time < min_time * 3, "Performance should be consistent across runs"
        assert avg_time < 5.0, f"Average analysis time too slow: {avg_time:.2f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])