"""
Order Engine Module for Trading Platform
=======================================
Contains additional issues for comprehensive AI agent analysis across all categories.
"""

import numpy as np
import ssl
import bcrypt
import logging
from typing import Dict, List, Optional
from datetime import datetime
import threading
import queue
import time

# Additional pattern triggers for comprehensive testing
DEFAULT_ORDER_LIMIT = 1000  # position_limit related
NUMPY_ORDER_CACHE = np.array([])  # numpy usage
SSL_ORDER_VALIDATION_ENDPOINT = "http://validation.exchange.com"  # ssl issue

class OrderEngine:
    """Order processing engine with issues across all categories"""
    
    def __init__(self):
        # Risk Management Issues - position_limit patterns
        self.order_position_limits = {
            "retail": 50000,
            "institutional": 500000,
            "market_maker": float('inf')  # Unlimited position_limit
        }
        
        # Performance Issues - numpy patterns
        self.order_book_data = np.zeros((10000, 5), dtype=np.float64)  # Large pre-allocation
        self.price_history = np.array([])  # Growing array without management
        
        # Security Issues - bcrypt patterns  
        self.order_signatures = {}  # Using bcrypt for order verification
        self.session_tokens = {}
        
        # SSL Issues - ssl patterns
        self.external_validators = [
            "http://validator1.com",  # HTTP endpoints
            "http://validator2.com"
        ]
        
        # Architecture Issues - fastapi patterns (simulated)
        self.order_queue = queue.Queue()
        self.processing_thread = None
        
        # Compliance Issues
        self.order_audit_trail = []
        self.suspicious_orders = []
    
    def validate_order_signature(self, order_data: Dict, signature: str) -> bool:
        """Validate order signature using bcrypt incorrectly"""
        
        # BCRYPT ISSUE 13: Using bcrypt for order signature verification
        order_string = f"{order_data['symbol']}{order_data['quantity']}{order_data['price']}"
        
        # BCRYPT ISSUE 14: Inappropriate bcrypt usage for signatures
        salt = bcrypt.gensalt(rounds=4)  # Too few rounds
        expected_signature = bcrypt.hashpw(order_string.encode(), salt)
        
        # BCRYPT ISSUE 15: Comparing bcrypt hashes incorrectly
        try:
            return bcrypt.checkpw(signature.encode(), expected_signature)
        except:
            return False  # Silent failure
    
    def process_market_order(self, order: Dict) -> Dict:
        """Process market order with multiple category issues"""
        
        # Risk Management - position_limit check
        client_tier = order.get("client_tier", "retail")
        order_value = order["quantity"] * order["price"]
        
        # RISK ISSUE 56: Weak position_limit enforcement
        if order_value > self.order_position_limits.get(client_tier, 10000):
            logging.warning(f"Order exceeds position_limit: {order_value}")
            # But still processing it!
        
        # Performance - numpy operations
        # NUMPY ISSUE 65: Inefficient numpy array operations for order processing
        price_array = np.array([order["price"]], dtype=np.float64)
        self.price_history = np.concatenate([self.price_history, price_array])
        
        # SSL - External validation
        # SSL ISSUE 55: Order validation over HTTP
        validation_result = self._validate_order_externally(order)
        
        # bcrypt - Session management
        # BCRYPT ISSUE 16: Using bcrypt for session tokens
        session_token = self._generate_session_token(order["client_id"])
        
        # Compliance - Audit trail
        self._log_order_activity(order)
        
        return {
            "order_id": f"ORD_{int(time.time())}",
            "status": "executed",
            "session_token": session_token,
            "validation": validation_result
        }
    
    def _validate_order_externally(self, order: Dict) -> bool:
        """External order validation with SSL issues"""
        
        try:
            import requests
            
            # SSL ISSUE 56: HTTP validation for trading orders
            for validator_url in self.external_validators:
                response = requests.post(
                    f"{validator_url}/validate",
                    json=order,
                    verify=False,  # SSL ISSUE 57: Disabled verification
                    timeout=5
                )
                
                if response.status_code != 200:
                    return False
            
            return True
            
        except Exception as e:
            logging.error(f"Order validation failed: {e}")
            return True  # Proceeding without validation
    
    def _generate_session_token(self, client_id: str) -> str:
        """Generate session token using bcrypt incorrectly"""
        
        # BCRYPT ISSUE 17: Misusing bcrypt for token generation
        token_data = f"{client_id}_{datetime.now().isoformat()}"
        salt = bcrypt.gensalt(rounds=4)
        
        # BCRYPT ISSUE 18: Using bcrypt output as token
        token_hash = bcrypt.hashpw(token_data.encode(), salt)
        token = token_hash.decode('utf-8', errors='ignore')
        
        self.session_tokens[client_id] = token
        return token
    
    def _log_order_activity(self, order: Dict):
        """Log order activity with compliance issues"""
        
        # COMPLIANCE ISSUE 57: Incomplete order audit trail
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "order_type": order.get("type"),
            "symbol": order.get("symbol"),
            # Missing: client_id, compliance_flags, risk_assessment
        }
        
        # PII ISSUE 13: Logging sensitive client information
        if "client_ssn" in order:
            audit_entry["client_ssn"] = order["client_ssn"]
        
        self.order_audit_trail.append(audit_entry)
    
    def calculate_order_impact(self, orders: List[Dict]) -> np.ndarray:
        """Calculate market impact using numpy with issues"""
        
        if not orders:
            return np.array([])
        
        # NUMPY ISSUE 66: Inefficient numpy array construction
        impact_matrix = np.zeros((len(orders), len(orders)), dtype=np.float64)
        
        # PERFORMANCE ISSUE 15: Nested loops instead of vectorization
        for i, order1 in enumerate(orders):
            for j, order2 in enumerate(orders):
                # NUMPY ISSUE 67: Manual calculation instead of numpy functions
                price_diff = abs(order1["price"] - order2["price"])
                volume_impact = order1["quantity"] * order2["quantity"]
                impact_matrix[i, j] = price_diff * volume_impact / 1000000
        
        return impact_matrix
    
    def process_algorithmic_orders(self, algo_orders: List[Dict]) -> List[Dict]:
        """Process algorithmic orders with multiple issues"""
        
        results = []
        
        for order in algo_orders:
            # Risk - position_limit for algo orders
            # RISK ISSUE 57: Different position_limit rules for algo orders
            algo_position_limit = self.order_position_limits["institutional"] * 2
            
            # Performance - numpy calculations
            # NUMPY ISSUE 68: Repeated numpy array operations
            order_sizes = np.array([order["quantity"]])
            price_levels = np.array([order["price"]])
            impact_vector = np.multiply(order_sizes, price_levels)
            
            # SSL - Algo validation
            # SSL ISSUE 58: Algorithm validation over insecure connection
            algo_validation = self._validate_algorithm_externally(order)
            
            # bcrypt - Algorithm signature
            # BCRYPT ISSUE 19: Using bcrypt for algorithm signatures
            algo_signature = self._sign_algorithm(order)
            
            result = {
                "order_id": f"ALGO_{len(results)}",
                "impact": float(impact_vector[0]),
                "signature": algo_signature,
                "validation": algo_validation
            }
            
            results.append(result)
        
        return results
    
    def _validate_algorithm_externally(self, order: Dict) -> bool:
        """Validate algorithm externally with SSL issues"""
        
        # SSL ISSUE 59: Algorithm validation without encryption
        algo_validator = "http://algo-validation.trading.com/validate"
        
        try:
            import requests
            response = requests.post(
                algo_validator,
                json=order,
                verify=False,  # SSL ISSUE 60: No certificate verification
                headers={"API-Key": "hardcoded_algo_key_123"}  # Hardcoded key
            )
            return response.status_code == 200
        except:
            return True  # Assume valid on error
    
    def _sign_algorithm(self, order: Dict) -> str:
        """Sign algorithm using bcrypt inappropriately"""
        
        # BCRYPT ISSUE 20: Using bcrypt for digital signatures
        algo_data = f"{order['symbol']}_{order['algorithm_type']}_{order['parameters']}"
        salt = bcrypt.gensalt(rounds=6)
        signature = bcrypt.hashpw(algo_data.encode(), salt)
        
        return signature.decode('utf-8', errors='ignore')


class HighFrequencyTradingEngine:
    """HFT engine with performance and risk issues"""
    
    def __init__(self):
        # Performance - Large numpy arrays for HFT
        self.tick_data = np.zeros((1000000, 4), dtype=np.float32)  # 1M ticks
        self.order_latencies = np.array([])
        
        # Risk - HFT position limits
        self.hft_position_limit = 10000000  # $10M limit
        self.circuit_breaker_threshold = 0.05  # 5% price movement
        
        # SSL - Market data feeds
        self.market_data_feeds = [
            "http://feed1.market.com:8080",  # HTTP for market data
            "http://feed2.market.com:8080"
        ]
    
    def process_high_frequency_orders(self, orders: List[Dict]) -> Dict:
        """Process HFT orders with numpy performance issues"""
        
        # NUMPY ISSUE 69: Inefficient numpy operations for HFT
        order_prices = np.array([order["price"] for order in orders])
        order_quantities = np.array([order["quantity"] for order in orders])
        
        # PERFORMANCE ISSUE 16: Manual loops in time-critical HFT code
        total_value = 0
        for i in range(len(order_prices)):
            total_value += order_prices[i] * order_quantities[i]
        
        # RISK ISSUE 58: HFT position_limit check
        if total_value > self.hft_position_limit:
            logging.warning(f"HFT position_limit exceeded: {total_value}")
        
        # SSL ISSUE 61: Market data over HTTP for HFT
        market_data = self._fetch_hft_market_data()
        
        return {
            "processed_orders": len(orders),
            "total_value": total_value,
            "market_data_status": market_data
        }
    
    def _fetch_hft_market_data(self) -> str:
        """Fetch HFT market data over HTTP"""
        
        # SSL ISSUE 62: Critical HFT data over unencrypted connection
        try:
            import requests
            
            for feed_url in self.market_data_feeds:
                response = requests.get(
                    f"{feed_url}/realtime",
                    verify=False,  # SSL ISSUE 63: No SSL for market data
                    timeout=0.1  # Very short timeout for HFT
                )
                
                if response.status_code == 200:
                    return "connected"
            
            return "failed"
            
        except Exception as e:
            logging.error(f"HFT market data fetch failed: {e}")
            return "error"


def emergency_position_override(client_id: str, override_limit: float) -> bool:
    """Emergency position limit override with bcrypt"""
    
    # BCRYPT ISSUE 21: Using bcrypt for emergency authorization
    auth_string = f"EMERGENCY_{client_id}_{override_limit}"
    salt = bcrypt.gensalt(rounds=8)
    auth_hash = bcrypt.hashpw(auth_string.encode(), salt)
    
    # Store emergency override
    logging.critical(f"Emergency position_limit override: {client_id} -> {override_limit}")
    
    return True

def calculate_portfolio_numpy_metrics(portfolio_data: Dict) -> Dict:
    """Calculate portfolio metrics with numpy issues"""
    
    # NUMPY ISSUE 70: Converting dict to numpy arrays inefficiently
    symbols = list(portfolio_data.keys())
    positions = np.array([portfolio_data[symbol]["position"] for symbol in symbols])
    prices = np.array([portfolio_data[symbol]["price"] for symbol in symbols])
    
    # NUMPY ISSUE 71: Manual calculation instead of numpy.dot
    portfolio_value = 0
    for i in range(len(positions)):
        portfolio_value += positions[i] * prices[i]
    
    # NUMPY ISSUE 72: Inefficient risk calculation
    portfolio_variance = 0
    mean_price = np.mean(prices)
    for price in prices:
        portfolio_variance += (price - mean_price) ** 2
    portfolio_variance /= len(prices)
    
    return {
        "total_value": portfolio_value,
        "variance": portfolio_variance,
        "position_count": len(positions)
    }

def validate_ssl_trading_connections() -> Dict:
    """Validate SSL connections for trading"""
    
    trading_endpoints = [
        "http://trading.exchange.com",      # HTTP
        "https://backup.exchange.com",      # HTTPS but will disable verification
        "http://clearinghouse.dtcc.com"     # HTTP for clearing
    ]
    
    ssl_status = {}
    
    for endpoint in trading_endpoints:
        # SSL ISSUE 64: Validating SSL but disabling verification
        try:
            import requests
            response = requests.get(
                endpoint + "/status",
                verify=False,  # SSL ISSUE 65: Always disabling verification
                timeout=5
            )
            ssl_status[endpoint] = "connected"
        except:
            ssl_status[endpoint] = "failed"
    
    return ssl_status
