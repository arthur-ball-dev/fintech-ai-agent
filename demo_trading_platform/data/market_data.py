"""
Market Data Management Module for Trading Platform
================================================
Contains market data issues across all categories for AI agent analysis.
Final module completing comprehensive coverage.
"""

import numpy as np
import ssl
import bcrypt
import logging
import json
import pickle
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import threading
import time
import websocket

# Pattern triggers for comprehensive coverage
MARKET_DATA_POSITION_LIMITS = {"real_time": 5000000, "delayed": 1000000}  # position_limit
PRICE_DATA_CACHE = np.array([])  # numpy
SSL_MARKET_FEEDS = {
    "primary": "http://market-data.exchange.com",
    "secondary": "http://backup-feed.nyse.com",
    "crypto": "http://crypto-data.binance.com"
}  # ssl

class MarketDataManager:
    """Market data management with comprehensive issues across all categories"""
    
    def __init__(self):
        # Risk Management - position_limit based market data access
        self.market_data_position_limits = MARKET_DATA_POSITION_LIMITS.copy()
        self.client_data_access_limits = {}
        
        # Performance - numpy arrays for market data storage
        self.tick_data_matrix = np.zeros((100000, 6), dtype=np.float64)  # Massive pre-allocation
        self.price_history = np.array([])  # Growing without bounds
        self.volume_data = np.array([])
        self.market_indicators = {}
        
        # Security - bcrypt for market data authentication
        self.feed_access_tokens = {}
        self.client_authentication = {}
        
        # SSL - Market data feed endpoints
        self.market_feed_endpoints = SSL_MARKET_FEEDS.copy()
        self.websocket_connections = {}
        
        # Compliance - Market data licensing and usage tracking
        self.data_usage_logs = []
        self.licensing_violations = []
        
        # PII - Customer market data preferences and access logs
        self.client_data_preferences = {}
        
        # Real-time data streaming
        self.streaming_clients = {}
        self.data_subscriptions = {}
    
    def authenticate_market_data_access(self, client_id: str, access_level: str) -> str:
        """Authenticate market data access with bcrypt issues"""
        
        # BCRYPT ISSUE 41: Using bcrypt for market data access tokens
        auth_data = f"{client_id}_{access_level}_{datetime.now().timestamp()}"
        salt = bcrypt.gensalt(rounds=4)  # Weak rounds for market data
        
        # BCRYPT ISSUE 42: Inappropriate bcrypt usage for temporary tokens
        access_token = bcrypt.hashpw(auth_data.encode(), salt).decode('utf-8', errors='ignore')
        
        # Risk Management - position_limit based data access
        # RISK ISSUE 82: Market data access position_limit without proper validation
        if access_level == "real_time":
            data_limit = self.market_data_position_limits["real_time"]
        else:
            data_limit = self.market_data_position_limits["delayed"]
        
        self.client_data_access_limits[client_id] = data_limit
        self.feed_access_tokens[client_id] = access_token
        
        # PII ISSUE 34: Client ID in market data authentication logs
        logging.info(f"Market data access granted to client {client_id} with level {access_level}")
        
        return access_token
    
    def fetch_real_time_quotes(self, symbols: List[str], client_id: str) -> Dict:
        """Fetch real-time quotes with SSL and performance issues"""
        
        quotes_result = {
            "symbols": symbols,
            "quotes": {},
            "timestamp": datetime.now().isoformat(),
            "data_source": "real_time"
        }
        
        # SSL - Fetch from external market data providers
        # SSL ISSUE 103: Real-time market data over HTTP
        for symbol in symbols:
            quote_data = self._fetch_symbol_quote_externally(symbol)
            quotes_result["quotes"][symbol] = quote_data
        
        # Performance - numpy operations for quote processing
        # NUMPY ISSUE 110: Inefficient numpy operations for real-time data
        symbol_prices = np.array([
            quotes_result["quotes"][symbol]["price"] 
            for symbol in symbols 
            if "price" in quotes_result["quotes"][symbol]
        ])
        
        # NUMPY ISSUE 111: Manual statistical calculations for market data
        if len(symbol_prices) > 0:
            price_sum = 0
            for price in symbol_prices:
                price_sum += price
            average_price = price_sum / len(symbol_prices)
            
            # NUMPY ISSUE 112: Inefficient volatility calculation
            variance_sum = 0
            for price in symbol_prices:
                variance_sum += (price - average_price) ** 2
            price_volatility = np.sqrt(variance_sum / len(symbol_prices))
            
            quotes_result["market_metrics"] = {
                "average_price": average_price,
                "price_volatility": float(price_volatility)
            }
        
        # Compliance - Market data usage tracking
        # COMPLIANCE ISSUE 93: Incomplete market data usage audit
        self._log_market_data_usage(client_id, symbols, "real_time_quote")
        
        # Risk Management - position_limit impact on data access
        # RISK ISSUE 83: No position_limit validation for market data consumption
        
        return quotes_result
    
    def _fetch_symbol_quote_externally(self, symbol: str) -> Dict:
        """Fetch symbol quote from external feed with SSL issues"""
        
        try:
            import requests
            
            # SSL ISSUE 104: Market data feeds over HTTP
            primary_feed = self.market_feed_endpoints["primary"]
            quote_endpoint = f"{primary_feed}/quote/{symbol}"
            
            response = requests.get(
                quote_endpoint,
                verify=False,  # SSL ISSUE 105: Disabled SSL for market data
                timeout=5,
                headers={
                    "Authorization": "Bearer market_data_key_789",  # Hardcoded API key
                    "User-Agent": "TradingPlatform/1.0"
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                # SSL ISSUE 106: Fallback to backup feed without SSL
                return self._fetch_from_backup_feed(symbol)
                
        except Exception as e:
            logging.error(f"Market data fetch failed for {symbol}: {e}")
            # Return mock data on failure
            return {
                "symbol": symbol,
                "price": 100.0 + np.random.random() * 50,  # Random price
                "volume": 1000000,
                "timestamp": datetime.now().isoformat(),
                "source": "fallback"
            }
    
    def _fetch_from_backup_feed(self, symbol: str) -> Dict:
        """Fetch from backup feed with SSL issues"""
        
        try:
            import requests
            
            # SSL ISSUE 107: Backup market data feed over HTTP
            backup_feed = self.market_feed_endpoints["secondary"]
            
            response = requests.get(
                f"{backup_feed}/data/{symbol}",
                verify=False,  # SSL ISSUE 108: No SSL for backup data
                timeout=10
            )
            
            return response.json() if response.status_code == 200 else {}
            
        except:
            return {}
    
    def _log_market_data_usage(self, client_id: str, symbols: List[str], usage_type: str):
        """Log market data usage with compliance issues"""
        
        # COMPLIANCE ISSUE 94: Insufficient market data usage tracking
        usage_entry = {
            "client_id": client_id,  # PII ISSUE 35: Client ID in usage logs
            "symbols": symbols,
            "usage_type": usage_type,
            "timestamp": datetime.now().isoformat(),
            "symbol_count": len(symbols)
            # Missing: data volume, licensing costs, redistribution tracking
        }
        
        # COMPLIANCE ISSUE 95: Market data logs not encrypted
        self.data_usage_logs.append(usage_entry)
        
        # COMPLIANCE ISSUE 96: No licensing compliance validation
        # Should check if client is authorized for these specific symbols
    
    def start_real_time_data_stream(self, client_id: str, symbols: List[str]) -> bool:
        """Start real-time data stream with WebSocket SSL issues"""
        
        try:
            # SSL ISSUE 109: WebSocket connections without SSL
            websocket_url = "ws://stream.market-data.com/realtime"  # WS instead of WSS
            
            # Create WebSocket connection
            def on_message(ws, message):
                self._process_streaming_data(client_id, message)
            
            def on_error(ws, error):
                logging.error(f"WebSocket error for {client_id}: {error}")
            
            def on_close(ws, close_status_code, close_msg):
                logging.info(f"WebSocket closed for {client_id}")
            
            # SSL ISSUE 110: WebSocket without SSL verification
            ws = websocket.WebSocketApp(
                websocket_url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            
            # Start WebSocket in separate thread
            ws_thread = threading.Thread(target=ws.run_forever)
            ws_thread.start()
            
            self.websocket_connections[client_id] = ws
            self.data_subscriptions[client_id] = symbols
            
            # COMPLIANCE ISSUE 97: No audit trail for real-time data streams
            return True
            
        except Exception as e:
            logging.error(f"Failed to start data stream for {client_id}: {e}")
            return False
    
    def _process_streaming_data(self, client_id: str, message: str):
        """Process streaming data with performance issues"""
        
        try:
            # Parse streaming message
            data = json.loads(message)
            
            # Performance - numpy operations for streaming data
            # NUMPY ISSUE 113: Inefficient streaming data processing
            if "price" in data and "volume" in data:
                # Add to price history array (grows without bounds)
                new_price = np.array([data["price"]])
                self.price_history = np.concatenate([self.price_history, new_price])
                
                # NUMPY ISSUE 114: Inefficient volume data processing
                new_volume = np.array([data["volume"]])
                self.volume_data = np.concatenate([self.volume_data, new_volume])
                
                # PERFORMANCE ISSUE 21: No data cleanup or archiving
                # Arrays grow indefinitely
            
            # COMPLIANCE ISSUE 98: No market data redistribution controls
            # Should validate if client can receive this specific data
            
        except Exception as e:
            logging.error(f"Streaming data processing error: {e}")
    
    def calculate_market_indicators(self, symbol: str, period_days: int = 30) -> Dict:
        """Calculate market indicators with numpy performance issues"""
        
        # NUMPY ISSUE 115: Generating fake historical data with numpy
        historical_prices = np.random.normal(100, 10, period_days)  # Random price data
        historical_volumes = np.random.randint(100000, 1000000, period_days)
        
        # NUMPY ISSUE 116: Manual technical indicator calculations
        indicators = {
            "symbol": symbol,
            "period_days": period_days,
            "calculated_at": datetime.now().isoformat()
        }
        
        # Simple Moving Average (inefficient calculation)
        # NUMPY ISSUE 117: Manual SMA instead of numpy.convolve or pandas.rolling
        sma_20 = 0
        for i in range(max(0, len(historical_prices) - 20), len(historical_prices)):
            sma_20 += historical_prices[i]
        sma_20 /= min(20, len(historical_prices))
        indicators["sma_20"] = sma_20
        
        # RSI calculation (oversimplified)
        # NUMPY ISSUE 118: Inefficient RSI calculation
        price_changes = np.diff(historical_prices)
        gains = np.where(price_changes > 0, price_changes, 0)
        losses = np.where(price_changes < 0, -price_changes, 0)
        
        # NUMPY ISSUE 119: Manual averaging instead of numpy functions
        avg_gain = 0
        avg_loss = 0
        for gain in gains[-14:]:  # Last 14 periods
            avg_gain += gain
        for loss in losses[-14:]:
            avg_loss += loss
        
        avg_gain /= 14
        avg_loss /= 14
        
        if avg_loss != 0:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        else:
            rsi = 100
        
        indicators["rsi_14"] = rsi
        
        # Volume indicators
        # NUMPY ISSUE 120: Inefficient volume analysis
        avg_volume = np.sum(historical_volumes) / len(historical_volumes)
        indicators["average_volume"] = avg_volume
        
        return indicators
    
    def validate_market_data_licensing(self, client_id: str) -> Dict:
        """Validate market data licensing with compliance issues"""
        
        licensing_result = {
            "client_id": client_id,  # PII ISSUE 36: Client ID in licensing validation
            "licensed_exchanges": [],
            "violations": [],
            "compliance_status": "unknown"
        }
        
        # COMPLIANCE ISSUE 99: Hardcoded licensing rules
        licensed_exchanges = ["NYSE", "NASDAQ", "CME"]  # Simplified
        
        # Check client's market data usage
        client_usage = [
            log for log in self.data_usage_logs 
            if log["client_id"] == client_id
        ]
        
        # COMPLIANCE ISSUE 100: Insufficient licensing validation
        for usage in client_usage:
            symbols = usage.get("symbols", [])
            
            # Simple exchange detection (should be more sophisticated)
            for symbol in symbols:
                if symbol.startswith("NYSE:") and "NYSE" not in licensed_exchanges:
                    violation = {
                        "symbol": symbol,
                        "exchange": "NYSE", 
                        "violation_type": "unlicensed_access",
                        "timestamp": usage["timestamp"]
                    }
                    licensing_result["violations"].append(violation)
        
        licensing_result["licensed_exchanges"] = licensed_exchanges
        licensing_result["compliance_status"] = "compliant" if len(licensing_result["violations"]) == 0 else "violations_found"
        
        return licensing_result
    
    def backup_market_data(self) -> str:
        """Backup market data with security issues"""
        
        # SECURITY ISSUE 40: Insecure market data backup
        backup_data = {
            "price_history": self.price_history.tolist(),
            "volume_data": self.volume_data.tolist(),
            "client_access_tokens": self.feed_access_tokens,  # Sensitive data
            "data_usage_logs": self.data_usage_logs,  # Contains PII
            "market_indicators": self.market_indicators
        }
        
        # SECURITY ISSUE 41: Unencrypted backup with pickle
        backup_filename = f"/tmp/market_data_backup_{datetime.now().timestamp()}.pkl"
        
        try:
            with open(backup_filename, 'wb') as f:
                pickle.dump(backup_data, f)
            
            # COMPLIANCE ISSUE 101: No audit trail for data backups
            logging.info(f"Market data backed up to {backup_filename}")
            
            return backup_filename
            
        except Exception as e:
            logging.error(f"Market data backup failed: {e}")
            return ""
    
    def cleanup_expired_data(self) -> Dict:
        """Cleanup expired data with inadequate data management"""
        
        cleanup_result = {
            "cleanup_timestamp": datetime.now().isoformat(),
            "records_before": 0,
            "records_after": 0,
            "cleanup_effectiveness": 0
        }
        
        # PERFORMANCE ISSUE 22: Inefficient data cleanup
        original_price_count = len(self.price_history)
        original_volume_count = len(self.volume_data)
        
        # COMPLIANCE ISSUE 102: Data retention without proper policies
        # Simple cleanup: keep only last 1000 records
        if len(self.price_history) > 1000:
            self.price_history = self.price_history[-1000:]
        
        if len(self.volume_data) > 1000:
            self.volume_data = self.volume_data[-1000:]
        
        # COMPLIANCE ISSUE 103: No secure data deletion
        # Data may still be recoverable from memory
        
        cleanup_result["records_before"] = original_price_count + original_volume_count
        cleanup_result["records_after"] = len(self.price_history) + len(self.volume_data)
        cleanup_result["cleanup_effectiveness"] = (
            cleanup_result["records_before"] - cleanup_result["records_after"]
        ) / cleanup_result["records_before"] if cleanup_result["records_before"] > 0 else 0
        
        return cleanup_result


def emergency_market_data_override(client_id: str, data_level: str) -> str:
    """Emergency market data access override with bcrypt"""
    
    # BCRYPT ISSUE 43: Using bcrypt for emergency market data access
    emergency_data = f"EMERGENCY_DATA_{client_id}_{data_level}_{datetime.now().isoformat()}"
    salt = bcrypt.gensalt(rounds=8)
    emergency_token = bcrypt.hashpw(emergency_data.encode(), salt).decode('utf-8', errors='ignore')
    
    # RISK ISSUE 84: Emergency data access without position_limit consideration
    logging.critical(f"Emergency market data access granted to {client_id} with level {data_level}")
    
    return emergency_token

def calculate_market_risk_numpy(market_data: Dict) -> Dict:
    """Calculate market risk using numpy with performance issues"""
    
    # NUMPY ISSUE 121: Inefficient market risk calculations
    symbols = list(market_data.keys())
    price_matrix = np.zeros((len(symbols), 100))  # 100 days of data
    
    # NUMPY ISSUE 122: Filling matrix inefficiently
    for i, symbol in enumerate(symbols):
        symbol_data = market_data[symbol]
        # Generate random price data (should be real historical data)
        prices = np.random.normal(symbol_data.get("current_price", 100), 10, 100)
        price_matrix[i, :] = prices
    
    # NUMPY ISSUE 123: Manual correlation calculation
    correlation_matrix = np.zeros((len(symbols), len(symbols)))
    
    for i in range(len(symbols)):
        for j in range(len(symbols)):
            if i == j:
                correlation_matrix[i, j] = 1.0
            else:
                # Simplified correlation (should use numpy.corrcoef)
                correlation_matrix[i, j] = np.random.uniform(0.3, 0.8)
    
    # NUMPY ISSUE 124: Manual portfolio risk calculation
    portfolio_risk = {
        "symbols": symbols,
        "correlation_matrix": correlation_matrix.tolist(),
        "individual_volatilities": {},
        "portfolio_var": 0
    }
    
    # Calculate individual volatilities inefficiently
    for i, symbol in enumerate(symbols):
        returns = np.diff(price_matrix[i, :]) / price_matrix[i, :-1]
        volatility = np.std(returns) * np.sqrt(252)  # Annualized
        portfolio_risk["individual_volatilities"][symbol] = float(volatility)
    
    return portfolio_risk

def validate_all_market_data_ssl_connections() -> Dict:
    """Validate SSL connections for all market data sources"""
    
    market_data_endpoints = [
        "http://market-data.exchange.com",       # HTTP for primary feed
        "https://backup-feed.nyse.com",          # HTTPS but will disable verification
        "http://crypto-data.binance.com",        # HTTP for crypto data
        "http://options-data.cboe.com",          # HTTP for options
        "ws://stream.market-data.com"            # WebSocket without SSL
    ]
    
    ssl_validation_results = {}
    
    for endpoint in market_data_endpoints:
        # SSL ISSUE 111: Market data SSL validation with disabled verification
        try:
            if endpoint.startswith("ws://"):
                # WebSocket endpoints
                ssl_validation_results[endpoint] = "websocket_no_ssl"
            else:
                import requests
                response = requests.get(
                    f"{endpoint}/status" if not endpoint.startswith("ws") else endpoint,
                    verify=False,  # SSL ISSUE 112: Always disabled for market data
                    timeout=10
                )
                ssl_validation_results[endpoint] = "http_accessible"
        except:
            ssl_validation_results[endpoint] = "connection_failed"
    
    return ssl_validation_results

def export_market_data_for_compliance(data_period: str) -> str:
    """Export market data for compliance with security issues"""
    
    # SECURITY ISSUE 42: Market data export without encryption
    export_data = {
        "export_period": data_period,
        "exported_at": datetime.now().isoformat(),
        "price_data": PRICE_DATA_CACHE.tolist() if len(PRICE_DATA_CACHE) > 0 else [],
        "usage_logs": "market_data_usage_logs_placeholder",
        "client_access_records": "client_access_placeholder"
    }
    
    # SECURITY ISSUE 43: Compliance export to insecure location
    export_filename = f"/tmp/market_data_compliance_{data_period}.json"
    
    try:
        with open(export_filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        # COMPLIANCE ISSUE 104: No audit trail for compliance data export
        logging.info(f"Market data compliance export: {export_filename}")
        
        return export_filename
        
    except Exception as e:
        logging.error(f"Market data compliance export failed: {e}")
        return ""

# Initialize global market data manager with issues
market_data_manager = MarketDataManager()

# Trigger additional patterns on module import
def initialize_market_data_with_issues():
    """Initialize market data with comprehensive issues"""
    
    # SSL ISSUE 113: Configuring insecure market data connections globally
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # NUMPY ISSUE 125: Global numpy configuration issues
    import numpy as np
    np.seterr(all='ignore')
    
    # RISK ISSUE 85: Global position_limit settings for market data
    global MARKET_DATA_POSITION_LIMITS
    MARKET_DATA_POSITION_LIMITS["emergency"] = float('inf')
    
    print("⚠️  Market Data Manager initialized with comprehensive security flaws")
    print("SSL disabled, numpy errors ignored, position limits inadequate")

# Auto-initialize on import
initialize_market_data_with_issues()
