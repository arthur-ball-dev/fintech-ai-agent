"""
Test fixtures and sample data for FinTech analysis testing.

Provides reusable test data, mock LLM responses, and utility functions
for creating consistent test scenarios across the test suite.
"""
import tempfile
import os
from pathlib import Path
from typing import Dict, List
from unittest.mock import Mock


class FinTechTestData:
    """Generator for realistic FinTech test data."""
    
    @staticmethod
    def create_risk_management_code() -> str:
        """Generate sample risk management code with multiple patterns."""
        return """
import logging
import numpy as np
from datetime import datetime
from typing import Dict, List

# Position limits and risk controls
MAX_POSITION_SIZE = 1000000
STOP_LOSS_PERCENTAGE = 0.02
PORTFOLIO_VAR_LIMIT = 0.05

class RiskManager:
    def __init__(self):
        self.position_limits = {
            "equity": 500000,
            "fx": 250000,
            "commodity": 100000
        }
        self.max_daily_loss = 50000
    
    def check_position_limit(self, instrument_type: str, position_size: float) -> bool:
        \"\"\"Validate position against limits.\"\"\"
        limit = self.position_limits.get(instrument_type, 0)
        if position_size > limit:
            logging.error(f"Position {position_size} exceeds limit {limit} for {instrument_type}")
            return False
        return True
    
    def calculate_stop_loss(self, entry_price: float, risk_percentage: float = None) -> float:
        \"\"\"Calculate stop loss price.\"\"\"
        risk_pct = risk_percentage or STOP_LOSS_PERCENTAGE
        return entry_price * (1 - risk_pct)
    
    def calculate_portfolio_var(self, positions: List[float], confidence: float = 0.95) -> float:
        \"\"\"Calculate portfolio Value at Risk.\"\"\"
        if not positions:
            return 0.0
        
        returns = np.array(positions)
        var = np.percentile(returns, (1 - confidence) * 100)
        return abs(var)
    
    def validate_trade(self, trade_data: Dict) -> bool:
        \"\"\"Comprehensive trade validation.\"\"\"
        # Position size check
        if not self.check_position_limit(trade_data.get("type"), trade_data.get("size", 0)):
            return False
        
        # Risk/reward ratio check
        entry_price = trade_data.get("entry_price", 0)
        stop_loss = self.calculate_stop_loss(entry_price)
        risk_amount = abs(entry_price - stop_loss) * trade_data.get("quantity", 0)
        
        if risk_amount > self.max_daily_loss:
            logging.warning(f"Trade risk {risk_amount} exceeds daily limit {self.max_daily_loss}")
            return False
        
        return True
    
    def audit_trail(self, user_id: str, action: str, details: Dict = None):
        \"\"\"Create audit trail for compliance.\"\"\"
        timestamp = datetime.utcnow().isoformat()
        audit_data = {
            "timestamp": timestamp,
            "user_id": user_id,
            "action": action,
            "details": details or {}
        }
        logging.info(f"AUDIT: {audit_data}")

# Circuit breaker for operational risk
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
    
    def call(self, func, *args, **kwargs):
        \"\"\"Execute function with circuit breaker protection.\"\"\"
        if self._is_open():
            raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _is_open(self) -> bool:
        if self.failure_count >= self.failure_threshold:
            if self.last_failure_time:
                time_since_failure = datetime.now() - self.last_failure_time
                return time_since_failure.seconds < self.timeout
        return False
    
    def _on_success(self):
        self.failure_count = 0
        self.last_failure_time = None
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()

# Emergency stop mechanism
def emergency_stop(reason: str):
    \"\"\"Emergency trading halt.\"\"\"
    logging.critical(f"EMERGENCY STOP: {reason}")
    # In real system, would halt all trading
    pass

def rate_limit_check(user_id: str, action: str) -> bool:
    \"\"\"Rate limiting for API calls.\"\"\"
    # Simplified rate limiting logic
    return True
"""
    
    @staticmethod
    def create_performance_code() -> str:
        """Generate sample performance optimization code."""
        return """
import asyncio
import numpy as np
from collections import deque
import struct
import threading
from concurrent.futures import ThreadPoolExecutor
import time

# High-frequency trading optimizations
class FastMarketDataProcessor:
    __slots__ = ['_queue', '_buffer', '_processors', '_stats']
    
    def __init__(self, buffer_size: int = 10000):
        self._queue = deque(maxlen=buffer_size)
        self._buffer = bytearray(buffer_size * 8)
        self._processors = ThreadPoolExecutor(max_workers=4)
        self._stats = {"processed": 0, "errors": 0}
    
    async def process_tick(self, symbol: str, price: float, volume: int, timestamp: float):
        \"\"\"Process individual market tick with minimal latency.\"\"\"
        # Pack data for efficient storage
        packed_data = struct.pack('!fIf', price, volume, timestamp)
        
        # Add to queue for batch processing
        self._queue.append((symbol, packed_data))
        
        # Async processing to avoid blocking
        if len(self._queue) >= 1000:  # Batch size
            await self._process_batch()
    
    async def _process_batch(self):
        \"\"\"Process batch of market data asynchronously.\"\"\"
        batch = list(self._queue)
        self._queue.clear()
        
        # Use thread pool for CPU-intensive calculations
        future = self._processors.submit(self._calculate_metrics, batch)
        
        try:
            await asyncio.wrap_future(future, timeout=0.1)
            self._stats["processed"] += len(batch)
        except asyncio.TimeoutError:
            self._stats["errors"] += 1
    
    def _calculate_metrics(self, batch) -> dict:
        \"\"\"CPU-intensive calculations using numpy.\"\"\"
        if not batch:
            return {}
        
        # Extract prices for vectorized operations
        prices = []
        volumes = []
        
        for symbol, packed_data in batch:
            price, volume, timestamp = struct.unpack('!fIf', packed_data)
            prices.append(price)
            volumes.append(volume)
        
        # Vectorized calculations for performance
        prices_array = np.array(prices)
        volumes_array = np.array(volumes)
        
        return {
            "mean_price": np.mean(prices_array),
            "price_std": np.std(prices_array),
            "total_volume": np.sum(volumes_array),
            "vwap": np.sum(prices_array * volumes_array) / np.sum(volumes_array)
        }

# WebSocket connection optimizations
async def optimized_websocket_handler():
    \"\"\"Optimized WebSocket handling for real-time data.\"\"\"
    connection_pool = []
    
    async def handle_connection(websocket):
        try:
            async for message in websocket:
                # Minimal processing to reduce latency
                await process_message_fast(message)
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
    
    # Keep connections alive with minimal overhead
    while True:
        await asyncio.sleep(0.001)  # 1ms sleep for high frequency

async def process_message_fast(message):
    \"\"\"Ultra-fast message processing.\"\"\"
    # Minimal parsing and processing
    pass

# Memory-efficient data structures
class RingBuffer:
    \"\"\"Ring buffer for efficient price history storage.\"\"\"
    __slots__ = ['_buffer', '_size', '_index', '_count']
    
    def __init__(self, size: int):
        self._buffer = [0.0] * size
        self._size = size
        self._index = 0
        self._count = 0
    
    def append(self, value: float):
        self._buffer[self._index] = value
        self._index = (self._index + 1) % self._size
        self._count = min(self._count + 1, self._size)
    
    def get_array(self) -> np.ndarray:
        if self._count < self._size:
            return np.array(self._buffer[:self._count])
        else:
            # Return in correct order
            return np.concatenate([
                self._buffer[self._index:],
                self._buffer[:self._index]
            ])

# Performance monitoring
def perf_counter_ms() -> float:
    \"\"\"High-resolution performance counter in milliseconds.\"\"\"
    return time.perf_counter() * 1000

class LatencyMonitor:
    def __init__(self):
        self.latencies = deque(maxlen=1000)
    
    def record_latency(self, start_time: float):
        latency = perf_counter_ms() - start_time
        self.latencies.append(latency)
    
    def get_stats(self) -> dict:
        if not self.latencies:
            return {}
        
        latencies_array = np.array(self.latencies)
        return {
            "mean": np.mean(latencies_array),
            "p95": np.percentile(latencies_array, 95),
            "p99": np.percentile(latencies_array, 99),
            "max": np.max(latencies_array)
        }

# Anti-patterns (should be detected by analysis)
def slow_blocking_operation():
    \"\"\"This function will be flagged as a performance issue.\"\"\"
    time.sleep(0.1)  # Blocking sleep
    
def inefficient_loop(items):
    \"\"\"Inefficient loop pattern.\"\"\"
    result = []
    for i in range(len(items)):  # Should use enumerate or direct iteration
        result.append(process_item(items[i]))
    return result

def synchronous_http_calls():
    \"\"\"Synchronous HTTP calls that block execution.\"\"\"
    import requests
    response = requests.get("http://api.example.com")  # Should be async
    return response.json()
"""
    
    @staticmethod
    def create_compliance_code() -> str:
        """Generate sample compliance and security code."""
        return """
import bcrypt
import ssl
import hashlib
import logging
from datetime import datetime
from typing import Optional, Dict, List
import re

# Data protection and encryption
class DataProtectionManager:
    def __init__(self):
        self.encryption_key = self._generate_key()
        self.pii_fields = ['email', 'phone', 'ssn', 'credit_card']
    
    def encrypt_pii(self, data: str) -> bytes:
        \"\"\"Encrypt personally identifiable information.\"\"\"
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(data.encode('utf-8'), salt)
    
    def hash_sensitive_data(self, data: str) -> str:
        \"\"\"Hash sensitive data for GDPR compliance.\"\"\"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _generate_key(self) -> bytes:
        \"\"\"Generate encryption key securely.\"\"\"
        import secrets
        return secrets.token_bytes(32)
    
    def mask_pii(self, text: str) -> str:
        \"\"\"Mask PII in logs and outputs.\"\"\"
        # Email masking
        text = re.sub(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b', 
                     '***@***.***', text)
        
        # Phone number masking
        text = re.sub(r'\\b\\d{3}-?\\d{3}-?\\d{4}\\b', '***-***-****', text)
        
        return text

# SSL/TLS configuration
def setup_secure_ssl_context() -> ssl.SSLContext:
    \"\"\"Configure secure SSL context.\"\"\"
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')
    return context

# Input validation and sanitization
class InputValidator:
    @staticmethod
    def validate_sql_input(user_input: str) -> bool:
        \"\"\"Validate input to prevent SQL injection.\"\"\"
        dangerous_patterns = [
            r"('|(\\-\\-)|(;)|(\\||\\|)|(\\*|\\*))",
            r"(exec(\\s|\\+)+(s|x)p\\w+)",
            r"(union(\\s|\\+)+(all(\\s|\\+)+)?select)"
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return False
        return True
    
    @staticmethod
    def sanitize_xss(user_input: str) -> str:
        \"\"\"Sanitize input to prevent XSS attacks.\"\"\"
        # Basic HTML escaping
        user_input = user_input.replace('<', '&lt;')
        user_input = user_input.replace('>', '&gt;')
        user_input = user_input.replace('"', '&quot;')
        user_input = user_input.replace("'", '&#x27;')
        return user_input
    
    @staticmethod
    def validate_financial_amount(amount_str: str) -> bool:
        \"\"\"Validate financial amount format.\"\"\"
        pattern = r'^\\d+(\\.\\d{1,2})?$'
        return bool(re.match(pattern, amount_str))

# Audit logging for compliance
class ComplianceLogger:
    def __init__(self):
        self.logger = logging.getLogger('compliance')
        self.logger.setLevel(logging.INFO)
        
        # Configure handler for audit logs
        handler = logging.FileHandler('audit.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_transaction(self, user_id: str, transaction_type: str, 
                       amount: float, account_id: str):
        \"\"\"Log financial transaction for SOX compliance.\"\"\"
        self.logger.info(
            f"TRANSACTION: user_id={user_id}, type={transaction_type}, "
            f"amount={amount}, account={account_id}, "
            f"timestamp={datetime.utcnow().isoformat()}"
        )
    
    def log_access_attempt(self, user_id: str, resource: str, 
                          success: bool, ip_address: str):
        \"\"\"Log access attempts for security monitoring.\"\"\"
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(
            f"ACCESS: user_id={user_id}, resource={resource}, "
            f"status={status}, ip={ip_address}, "
            f"timestamp={datetime.utcnow().isoformat()}"
        )
    
    def log_pii_access(self, user_id: str, pii_type: str, customer_id: str):
        \"\"\"Log PII access for GDPR compliance.\"\"\"
        self.logger.info(
            f"PII_ACCESS: user_id={user_id}, pii_type={pii_type}, "
            f"customer_id={customer_id}, "
            f"timestamp={datetime.utcnow().isoformat()}"
        )

# Role-based access control
class RBACManager:
    def __init__(self):
        self.user_roles = {}
        self.role_permissions = {
            'trader': ['view_positions', 'create_orders', 'view_market_data'],
            'risk_manager': ['view_positions', 'view_risk_reports', 'set_limits'],
            'compliance_officer': ['view_audit_logs', 'view_all_transactions'],
            'admin': ['manage_users', 'view_system_logs', 'configure_system']
        }
    
    def assign_role(self, user_id: str, role: str):
        \"\"\"Assign role to user.\"\"\"
        if role in self.role_permissions:
            self.user_roles[user_id] = role
    
    def check_permission(self, user_id: str, permission: str) -> bool:
        \"\"\"Check if user has specific permission.\"\"\"
        user_role = self.user_roles.get(user_id)
        if not user_role:
            return False
        
        allowed_permissions = self.role_permissions.get(user_role, [])
        return permission in allowed_permissions
    
    def require_permission(self, permission: str):
        \"\"\"Decorator to require specific permission.\"\"\"
        def decorator(func):
            def wrapper(user_id: str, *args, **kwargs):
                if not self.check_permission(user_id, permission):
                    raise PermissionError(f"User {user_id} lacks permission: {permission}")
                return func(user_id, *args, **kwargs)
            return wrapper
        return decorator

# Security vulnerabilities (should be detected)
API_SECRET_KEY = "hardcoded-secret-123"  # Security risk
DATABASE_PASSWORD = "admin123"  # Security risk
DEBUG_MODE = True  # Should be False in production

def weak_password_hash(password: str) -> str:
    \"\"\"Weak password hashing (should be flagged).\"\"\"
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is weak

def insecure_random():
    \"\"\"Insecure random number generation.\"\"\"
    import random
    return random.random()  # Not cryptographically secure
"""
    
    @staticmethod
    def create_architecture_code() -> str:
        """Generate sample architecture and API code."""
        return """
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import redis
import asyncio
from typing import List, Dict, Optional
import uvicorn
from datetime import datetime
import json

# FastAPI application setup
app = FastAPI(
    title="Trading Platform API",
    description="High-performance trading platform with microservice architecture",
    version="1.0.0"
)

# CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trading.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Redis cache for performance
cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Security
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    \"\"\"Verify JWT token for authentication.\"\"\"
    # In real implementation, would verify JWT
    if not credentials.credentials.startswith('valid_token'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return credentials.credentials

# Health check endpoint
@app.get("/health")
async def health_check():
    \"\"\"Health check for load balancer.\"\"\"
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "trading-api"
    }

# Trading endpoints
@app.get("/api/v1/positions")
async def get_positions(token: str = Depends(verify_token)):
    \"\"\"Get current trading positions.\"\"\"
    # Check cache first
    cached_positions = cache.get("positions")
    if cached_positions:
        return {"positions": json.loads(cached_positions), "source": "cache"}
    
    # Simulate database query
    positions = [
        {"symbol": "AAPL", "quantity": 100, "avg_price": 150.50},
        {"symbol": "GOOGL", "quantity": 50, "avg_price": 2800.00}
    ]
    
    # Cache for 30 seconds
    cache.setex("positions", 30, json.dumps(positions))
    
    return {"positions": positions, "source": "database"}

@app.post("/api/v1/orders")
async def create_order(order_data: Dict, token: str = Depends(verify_token)):
    \"\"\"Create new trading order.\"\"\"
    # Rate limiting check
    user_id = order_data.get("user_id")
    rate_limit_key = f"rate_limit:{user_id}"
    
    current_requests = cache.get(rate_limit_key) or "0"
    if int(current_requests) > 100:  # 100 requests per minute
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    # Increment rate limit counter
    cache.incr(rate_limit_key)
    cache.expire(rate_limit_key, 60)  # Reset after 1 minute
    
    # Simulate order processing
    order_id = f"ord_{datetime.now().timestamp()}"
    
    return {
        "order_id": order_id,
        "status": "pending",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/market-data/{symbol}")
async def get_market_data(symbol: str, token: str = Depends(verify_token)):
    \"\"\"Get real-time market data.\"\"\"
    # Check cache for fresh data
    cache_key = f"market_data:{symbol}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data)
    
    # Simulate market data fetch
    market_data = {
        "symbol": symbol,
        "price": 150.25,
        "volume": 1000000,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Cache for 1 second (high frequency updates)
    cache.setex(cache_key, 1, json.dumps(market_data))
    
    return market_data

# WebSocket endpoint for real-time updates
@app.websocket("/ws/market-data")
async def websocket_endpoint(websocket):
    \"\"\"WebSocket for real-time market data streaming.\"\"\"
    await websocket.accept()
    
    try:
        while True:
            # Simulate real-time data
            data = {
                "symbol": "AAPL",
                "price": 150.25 + (asyncio.get_event_loop().time() % 1),
                "timestamp": datetime.utcnow().isoformat()
            }
            await websocket.send_json(data)
            await asyncio.sleep(0.1)  # 10 updates per second
    except Exception as e:
        print(f"WebSocket error: {e}")

# Database connection pool simulation
class DatabasePool:
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.connections = []
        self.active_connections = 0
    
    async def get_connection(self):
        \"\"\"Get database connection from pool.\"\"\"
        if self.active_connections < self.pool_size:
            self.active_connections += 1
            return f"connection_{self.active_connections}"
        else:
            # Wait for available connection
            await asyncio.sleep(0.01)
            return await self.get_connection()
    
    async def release_connection(self, connection):
        \"\"\"Release connection back to pool.\"\"\"
        self.active_connections -= 1

# Message queue simulation
class MessageQueue:
    def __init__(self):
        self.queue = asyncio.Queue(maxsize=1000)
    
    async def publish(self, message: Dict):
        \"\"\"Publish message to queue.\"\"\"
        await self.queue.put(message)
    
    async def consume(self):
        \"\"\"Consume messages from queue.\"\"\"
        while True:
            message = await self.queue.get()
            await self.process_message(message)
    
    async def process_message(self, message: Dict):
        \"\"\"Process individual message.\"\"\"
        # Simulate message processing
        await asyncio.sleep(0.001)

# Microservice configuration
MICROSERVICE_CONFIG = {
    "name": "trading-api",
    "version": "1.0.0",
    "port": 8000,
    "database": {
        "url": "postgresql://user:pass@localhost/trading",
        "pool_size": 10
    },
    "redis": {
        "url": "redis://localhost:6379/0"
    },
    "monitoring": {
        "metrics_endpoint": "/metrics",
        "health_endpoint": "/health"
    }
}

# Container health check
async def container_health_check():
    \"\"\"Health check for container orchestration.\"\"\"
    try:
        # Check database connectivity
        db_status = await check_database_connection()
        
        # Check Redis connectivity
        redis_status = cache.ping()
        
        if db_status and redis_status:
            return {"status": "healthy"}
        else:
            return {"status": "unhealthy"}
    except Exception:
        return {"status": "unhealthy"}

async def check_database_connection():
    \"\"\"Check database connectivity.\"\"\"
    # Simulate database health check
    return True

# Prometheus metrics endpoint (placeholder)
@app.get("/metrics")
async def metrics():
    \"\"\"Prometheus metrics endpoint.\"\"\"
    return {
        "http_requests_total": 1000,
        "http_request_duration_seconds": 0.05,
        "active_connections": 25
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""


class MockLLMResponses:
    """Mock LLM responses for testing."""
    
    @staticmethod
    def get_risk_analysis_response(prompt: str) -> str:
        """Mock LLM response for risk analysis."""
        if "analyze" in prompt.lower() and "risk" in prompt.lower():
            return '{"tool": "analyze_financial_risk_patterns", "args": {"project_path": "."}}'
        elif "terminate" in prompt.lower():
            return '{"tool": "terminate", "args": {"message": "Risk analysis complete"}}'
        else:
            return '{"tool": "read_project_file", "args": {"name": "risk_management.py"}}'
    
    @staticmethod
    def get_compliance_response(prompt: str) -> str:
        """Mock LLM response for compliance analysis."""
        if "compliance" in prompt.lower() or "security" in prompt.lower():
            return '{"tool": "analyze_regulatory_compliance", "args": {"project_path": "."}}'
        elif "terminate" in prompt.lower():
            return '{"tool": "terminate", "args": {"message": "Compliance analysis complete"}}'
        else:
            return '{"tool": "list_project_files", "args": {}}'
    
    @staticmethod
    def get_performance_response(prompt: str) -> str:
        """Mock LLM response for performance analysis."""
        if "performance" in prompt.lower() or "hft" in prompt.lower():
            return '{"tool": "analyze_hft_performance_patterns", "args": {"project_path": "."}}'
        elif "terminate" in prompt.lower():
            return '{"tool": "terminate", "args": {"message": "Performance analysis complete"}}'
        else:
            return '{"tool": "find_project_root", "args": {}}'


class TestEnvironmentSetup:
    """Utilities for setting up test environments."""
    
    @staticmethod
    def create_temp_fintech_project(include_patterns: List[str] = None) -> str:
        """Create temporary FinTech project with specified patterns."""
        temp_dir = tempfile.mkdtemp()
        
        # Default patterns to include
        if include_patterns is None:
            include_patterns = ["risk", "performance", "compliance", "architecture"]
        
        # Create files based on requested patterns
        if "risk" in include_patterns:
            with open(os.path.join(temp_dir, "risk_management.py"), 'w') as f:
                f.write(FinTechTestData.create_risk_management_code())
        
        if "performance" in include_patterns:
            with open(os.path.join(temp_dir, "performance_optimizer.py"), 'w') as f:
                f.write(FinTechTestData.create_performance_code())
        
        if "compliance" in include_patterns:
            with open(os.path.join(temp_dir, "compliance_module.py"), 'w') as f:
                f.write(FinTechTestData.create_compliance_code())
        
        if "architecture" in include_patterns:
            with open(os.path.join(temp_dir, "api_server.py"), 'w') as f:
                f.write(FinTechTestData.create_architecture_code())
        
        return temp_dir
    
    @staticmethod
    def create_mock_agent(agent_type: str = "risk_management"):
        """Create mock agent for testing."""
        mock_agent = Mock()
        mock_agent.goals = [Mock(name=f"Goal {i}", priority=i) for i in range(1, 4)]
        mock_agent.actions.get_actions.return_value = [
            Mock(name="read_project_file"),
            Mock(name="analyze_financial_risk_patterns"),
            Mock(name="terminate")
        ]
        return mock_agent
    
    @staticmethod
    def create_sample_memory_with_results():
        """Create mock memory with analysis results."""
        mock_memory = Mock()
        mock_memory.get_memories.return_value = [
            {"type": "user", "content": "Analyze risk patterns"},
            {"type": "assistant", "content": "Starting risk analysis"},
            {"type": "environment", "content": "Risk analysis complete"}
        ]
        return mock_memory


# Test data constants
SAMPLE_ANALYSIS_RESULTS = {
    "risk_analysis": """
🏦 FINANCIAL RISK MANAGEMENT ANALYSIS
=====================================
Project: .
Files Analyzed: 4
Risk Controls Score: 75.0/100

📊 RISK CONTROLS DETECTED:
✅ Position Limits: 3 instances
✅ Stop Loss: 2 instances
✅ Portfolio Risk: 1 instances
✅ Operational Risk: 2 instances
""",
    
    "performance_analysis": """
⚡ HIGH-FREQUENCY TRADING PERFORMANCE ANALYSIS
===========================================
Project: .
Files Analyzed: 4
Performance Score: 80/100
HFT Readiness: 75/100

🚀 PERFORMANCE OPTIMIZATIONS DETECTED:
✅ Latency Critical: 4 instances
✅ Memory Efficiency: 3 instances
✅ Network Optimization: 2 instances
""",
    
    "compliance_analysis": """
🏛️ REGULATORY COMPLIANCE & SECURITY ANALYSIS
==========================================
Project: .
Files Analyzed: 4
Compliance Score: 85/100
Files with PII: 2

📋 COMPLIANCE PATTERNS DETECTED:
✅ Data Protection: 4 instances
✅ Audit Logging: 3 instances
✅ Access Control: 2 instances
✅ Input Validation: 3 instances

⚠️ SECURITY RISKS DETECTED:
❌ Hardcoded Secrets: 2 instances
❌ Weak Crypto: 1 instances
"""
}