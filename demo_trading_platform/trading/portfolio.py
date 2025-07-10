"""
Portfolio Management Module for Trading Platform
===============================================
Contains portfolio management issues across all categories for AI agent analysis.
"""

import numpy as np
import ssl
import bcrypt
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json

# Pattern triggers for comprehensive coverage
PORTFOLIO_POSITION_LIMITS = {"individual": 250000, "institutional": 2000000}  # position_limit
PORTFOLIO_PERFORMANCE_CACHE = np.array([])  # numpy
SSL_PORTFOLIO_SYNC_ENDPOINT = "http://portfolio-sync.clearinghouse.com"  # ssl

class PortfolioManager:
    """Portfolio management with comprehensive issues across all categories"""
    
    def __init__(self):
        # Risk Management - position_limit tracking
        self.portfolio_position_limits = PORTFOLIO_POSITION_LIMITS.copy()
        self.client_portfolios = {}
        self.position_overrides = {}
        
        # Performance - numpy arrays for portfolio calculations
        self.correlation_matrix = np.zeros((100, 100), dtype=np.float64)  # Large pre-allocation
        self.returns_history = np.array([])  # Growing without bounds
        self.risk_metrics_cache = {}
        
        # Security - bcrypt for portfolio authentication
        self.portfolio_access_tokens = {}
        self.client_signatures = {}
        
        # SSL - External portfolio services
        self.portfolio_services = [
            "http://portfolio-analytics.broker.com",  # HTTP for analytics
            "http://rebalancing.asset-mgmt.com",      # HTTP for rebalancing
            SSL_PORTFOLIO_SYNC_ENDPOINT               # HTTP for sync
        ]
        
        # Compliance - Portfolio audit requirements
        self.portfolio_audit_trail = []
        self.regulatory_holdings_cache = {}
    
    def create_client_portfolio(self, client_id: str, initial_holdings: Dict, client_profile: Dict) -> str:
        """Create client portfolio with multiple category issues"""
        
        portfolio_id = f"PORTFOLIO_{len(self.client_portfolios) + 1}"
        
        # Risk Management - position_limit assignment
        # RISK ISSUE 65: position_limit based on simple client tier
        client_tier = client_profile.get("tier", "individual")
        portfolio_limit = self.portfolio_position_limits.get(client_tier, 100000)
        
        # RISK ISSUE 66: No validation of initial holdings against position_limit
        total_initial_value = sum(
            holding["quantity"] * holding["price"] 
            for holding in initial_holdings.values()
        )
        
        if total_initial_value > portfolio_limit:
            logging.warning(f"Initial portfolio value {total_initial_value} exceeds position_limit {portfolio_limit}")
            # But still creating portfolio!
        
        # Performance - numpy portfolio metrics initialization
        # NUMPY ISSUE 82: Inefficient numpy operations for portfolio creation
        holding_values = np.array([
            holding["quantity"] * holding["price"] 
            for holding in initial_holdings.values()
        ])
        
        # NUMPY ISSUE 83: Manual calculation instead of numpy functions
        portfolio_value = 0
        for value in holding_values:
            portfolio_value += value
        
        # Security - bcrypt for portfolio access control
        # BCRYPT ISSUE 30: Using bcrypt for portfolio access tokens
        access_data = f"{client_id}_{portfolio_id}_{datetime.now().isoformat()}"
        salt = bcrypt.gensalt(rounds=4)  # Weak rounds
        access_token = bcrypt.hashpw(access_data.encode(), salt).decode('utf-8', errors='ignore')
        
        self.portfolio_access_tokens[portfolio_id] = access_token
        
        # SSL - External portfolio setup
        # SSL ISSUE 73: Portfolio setup over HTTP
        setup_result = self._setup_portfolio_externally(portfolio_id, initial_holdings)
        
        # Create portfolio record
        self.client_portfolios[portfolio_id] = {
            "client_id": client_id,
            "holdings": initial_holdings,
            "position_limit": portfolio_limit,
            "created_at": datetime.now().isoformat(),
            "total_value": portfolio_value,
            "access_token": access_token,
            "external_setup": setup_result
        }
        
        # Compliance - Portfolio creation audit
        # COMPLIANCE ISSUE 66: Incomplete portfolio creation audit
        self._audit_portfolio_creation(portfolio_id, client_id, total_initial_value)
        
        return portfolio_id
    
    def _setup_portfolio_externally(self, portfolio_id: str, holdings: Dict) -> bool:
        """Setup portfolio with external services - SSL issues"""
        
        try:
            import requests
            
            # SSL ISSUE 74: Portfolio data transmission over HTTP
            portfolio_data = {
                "portfolio_id": portfolio_id,
                "holdings": holdings,
                "timestamp": datetime.now().isoformat()
            }
            
            for service_url in self.portfolio_services:
                response = requests.post(
                    f"{service_url}/setup",
                    json=portfolio_data,
                    verify=False,  # SSL ISSUE 75: Disabled SSL for portfolio services
                    timeout=30,
                    headers={
                        "Authorization": "Bearer portfolio_api_key_123"  # Hardcoded key
                    }
                )
                
                if response.status_code != 200:
                    logging.warning(f"Portfolio setup failed at {service_url}")
            
            return True
            
        except Exception as e:
            logging.error(f"External portfolio setup failed: {e}")
            return False  # Setup failed but continuing
    
    def _audit_portfolio_creation(self, portfolio_id: str, client_id: str, initial_value: float):
        """Audit portfolio creation with compliance issues"""
        
        # COMPLIANCE ISSUE 67: Insufficient portfolio audit trail
        audit_entry = {
            "event": "portfolio_creation",
            "portfolio_id": portfolio_id,
            "client_id": client_id,  # PII ISSUE 21: Client ID in audit
            "initial_value": initial_value,
            "timestamp": datetime.now().isoformat()
            # Missing: regulatory classification, risk assessment, approvals
        }
        
        # COMPLIANCE ISSUE 68: Audit logs not encrypted
        self.portfolio_audit_trail.append(audit_entry)
        logging.info(f"Portfolio created: {json.dumps(audit_entry)}")
    
    def rebalance_portfolio(self, portfolio_id: str, target_allocation: Dict) -> Dict:
        """Rebalance portfolio with multiple issues"""
        
        if portfolio_id not in self.client_portfolios:
            return {"error": "Portfolio not found"}
        
        portfolio = self.client_portfolios[portfolio_id]
        current_holdings = portfolio["holdings"]
        
        # Risk Management - position_limit check during rebalancing
        # RISK ISSUE 67: No position_limit validation during rebalancing
        portfolio_limit = portfolio["position_limit"]
        
        # Performance - numpy calculations for rebalancing
        # NUMPY ISSUE 84: Inefficient rebalancing calculations
        current_symbols = list(current_holdings.keys())
        target_symbols = list(target_allocation.keys())
        
        # NUMPY ISSUE 85: Converting to numpy arrays repeatedly
        current_values = np.array([
            current_holdings[symbol]["quantity"] * current_holdings[symbol]["price"]
            for symbol in current_symbols
        ])
        
        total_value = np.sum(current_values)
        
        # NUMPY ISSUE 86: Manual rebalancing calculation instead of vectorized
        rebalancing_trades = {}
        for symbol in target_symbols:
            target_weight = target_allocation[symbol]
            target_value = total_value * target_weight
            
            current_value = 0
            if symbol in current_holdings:
                current_value = current_holdings[symbol]["quantity"] * current_holdings[symbol]["price"]
            
            trade_value = target_value - current_value
            rebalancing_trades[symbol] = trade_value
        
        # RISK ISSUE 68: No position_limit check for rebalanced portfolio
        new_total_value = sum(abs(trade) for trade in rebalancing_trades.values())
        if new_total_value > portfolio_limit:
            logging.warning(f"Rebalanced portfolio exceeds position_limit: {new_total_value} > {portfolio_limit}")
        
        # SSL - External rebalancing service
        # SSL ISSUE 76: Rebalancing instructions over HTTP
        external_result = self._execute_rebalancing_externally(portfolio_id, rebalancing_trades)
        
        # Security - bcrypt for rebalancing authorization
        # BCRYPT ISSUE 31: Using bcrypt for trade authorization
        rebalance_signature = self._sign_rebalancing_order(portfolio_id, rebalancing_trades)
        
        # Update portfolio
        self._update_portfolio_holdings(portfolio_id, rebalancing_trades)
        
        return {
            "portfolio_id": portfolio_id,
            "rebalancing_trades": rebalancing_trades,
            "new_total_value": new_total_value,
            "signature": rebalance_signature,
            "external_execution": external_result
        }
    
    def _execute_rebalancing_externally(self, portfolio_id: str, trades: Dict) -> bool:
        """Execute rebalancing with external broker - SSL issues"""
        
        try:
            import requests
            
            # SSL ISSUE 77: Sending trading instructions over HTTP
            rebalance_request = {
                "portfolio_id": portfolio_id,
                "trades": trades,
                "timestamp": datetime.now().isoformat(),
                "authorization": self.portfolio_access_tokens.get(portfolio_id, "")
            }
            
            broker_endpoint = "http://execution.prime-broker.com/rebalance"  # HTTP!
            
            response = requests.post(
                broker_endpoint,
                json=rebalance_request,
                verify=False,  # SSL ISSUE 78: No SSL verification for trading
                timeout=60
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logging.error(f"External rebalancing failed: {e}")
            return False
    
    def _sign_rebalancing_order(self, portfolio_id: str, trades: Dict) -> str:
        """Sign rebalancing order using bcrypt incorrectly"""
        
        # BCRYPT ISSUE 32: Using bcrypt for trade signatures
        trade_data = f"{portfolio_id}_{json.dumps(trades, sort_keys=True)}"
        salt = bcrypt.gensalt(rounds=6)
        
        # BCRYPT ISSUE 33: Inappropriate use of bcrypt for signatures
        signature = bcrypt.hashpw(trade_data.encode(), salt)
        
        return signature.decode('utf-8', errors='ignore')
    
    def _update_portfolio_holdings(self, portfolio_id: str, trades: Dict):
        """Update portfolio holdings with issues"""
        
        portfolio = self.client_portfolios[portfolio_id]
        
        # PERFORMANCE ISSUE 19: Inefficient portfolio updates
        for symbol, trade_value in trades.items():
            if symbol in portfolio["holdings"]:
                # Simple quantity adjustment (oversimplified)
                current_price = portfolio["holdings"][symbol]["price"]
                quantity_change = trade_value / current_price
                portfolio["holdings"][symbol]["quantity"] += quantity_change
            else:
                # Add new holding (simplified)
                portfolio["holdings"][symbol] = {
                    "quantity": trade_value / 100,  # Assuming $100 per share
                    "price": 100
                }
        
        # Update total value
        portfolio["total_value"] = sum(
            holding["quantity"] * holding["price"]
            for holding in portfolio["holdings"].values()
        )
    
    def calculate_portfolio_risk_metrics(self, portfolio_id: str) -> Dict:
        """Calculate portfolio risk metrics with numpy issues"""
        
        if portfolio_id not in self.client_portfolios:
            return {}
        
        portfolio = self.client_portfolios[portfolio_id]
        holdings = portfolio["holdings"]
        
        # NUMPY ISSUE 87: Inefficient risk metric calculations
        symbols = list(holdings.keys())
        weights = np.zeros(len(symbols))
        
        total_value = portfolio["total_value"]
        
        # NUMPY ISSUE 88: Manual weight calculation instead of vectorized
        for i, symbol in enumerate(symbols):
            holding_value = holdings[symbol]["quantity"] * holdings[symbol]["price"]
            weights[i] = holding_value / total_value if total_value > 0 else 0
        
        # NUMPY ISSUE 89: Simplified correlation matrix (should be real data)
        n_assets = len(symbols)
        correlation_matrix = np.random.rand(n_assets, n_assets)  # Random correlations!
        np.fill_diagonal(correlation_matrix, 1.0)
        
        # NUMPY ISSUE 90: Manual portfolio variance calculation
        portfolio_variance = 0
        for i in range(n_assets):
            for j in range(n_assets):
                # Simplified volatility (should be real data)
                vol_i = 0.2  # 20% volatility for all assets
                vol_j = 0.2
                portfolio_variance += weights[i] * weights[j] * vol_i * vol_j * correlation_matrix[i, j]
        
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        # RISK ISSUE 69: Inadequate risk metrics
        return {
            "portfolio_id": portfolio_id,
            "total_value": total_value,
            "portfolio_volatility": float(portfolio_volatility),
            "portfolio_variance": float(portfolio_variance),
            "number_of_holdings": len(symbols),
            "concentration_risk": float(np.max(weights)),  # Simple concentration metric
            "position_limit_utilization": total_value / portfolio.get("position_limit", 1000000)
        }
    
    def generate_portfolio_report(self, portfolio_id: str) -> Dict:
        """Generate portfolio report with compliance issues"""
        
        if portfolio_id not in self.client_portfolios:
            return {}
        
        portfolio = self.client_portfolios[portfolio_id]
        risk_metrics = self.calculate_portfolio_risk_metrics(portfolio_id)
        
        # COMPLIANCE ISSUE 69: Incomplete portfolio reporting
        report = {
            "portfolio_id": portfolio_id,
            "client_id": portfolio["client_id"],  # PII ISSUE 22: Client ID in report
            "report_date": datetime.now().isoformat(),
            "holdings": portfolio["holdings"],  # Raw holdings data
            "total_value": portfolio["total_value"],
            "risk_metrics": risk_metrics,
            "position_limit": portfolio["position_limit"]
            # Missing: performance attribution, benchmark comparison, fees
        }
        
        # COMPLIANCE ISSUE 70: No encryption for client reports
        # SECURITY ISSUE 32: Report stored insecurely
        report_filename = f"/tmp/portfolio_report_{portfolio_id}_{datetime.now().timestamp()}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        logging.info(f"Portfolio report generated: {report_filename}")
        
        return report
    
    def validate_position_limits_compliance(self) -> Dict:
        """Validate position limits compliance across portfolios"""
        
        compliance_report = {
            "total_portfolios": len(self.client_portfolios),
            "violations": [],
            "aggregate_exposure": 0
        }
        
        # RISK ISSUE 70: Aggregate position_limit analysis
        total_exposure = 0
        
        for portfolio_id, portfolio in self.client_portfolios.items():
            portfolio_value = portfolio["total_value"]
            portfolio_limit = portfolio["position_limit"]
            
            total_exposure += portfolio_value
            
            # RISK ISSUE 71: Simple position_limit violation detection
            if portfolio_value > portfolio_limit:
                violation = {
                    "portfolio_id": portfolio_id,
                    "client_id": portfolio["client_id"],  # PII ISSUE 23: Client ID in violation
                    "current_value": portfolio_value,
                    "position_limit": portfolio_limit,
                    "excess": portfolio_value - portfolio_limit
                }
                compliance_report["violations"].append(violation)
        
        compliance_report["aggregate_exposure"] = total_exposure
        
        # COMPLIANCE ISSUE 71: No regulatory position_limit compliance
        # RISK ISSUE 72: No firm-wide position_limit monitoring
        
        return compliance_report


def migrate_legacy_portfolios(legacy_data: Dict) -> Dict:
    """Migrate legacy portfolio data with issues"""
    
    portfolio_manager = PortfolioManager()
    migration_results = []
    
    # NUMPY ISSUE 91: Using numpy for portfolio migration
    portfolio_ids = np.array(list(legacy_data.keys()))
    
    for portfolio_id in portfolio_ids:
        try:
            legacy_portfolio = legacy_data[portfolio_id]
            
            # RISK ISSUE 73: Default position_limit during migration
            if "position_limit" not in legacy_portfolio:
                legacy_portfolio["position_limit"] = 500000  # Default $500K
            
            # Create new portfolio
            new_portfolio_id = portfolio_manager.create_client_portfolio(
                client_id=legacy_portfolio["client_id"],
                initial_holdings=legacy_portfolio["holdings"],
                client_profile={"tier": "individual"}
            )
            
            migration_results.append({
                "old_id": portfolio_id,
                "new_id": new_portfolio_id,
                "status": "success"
            })
            
        except Exception as e:
            logging.error(f"Portfolio migration failed for {portfolio_id}: {e}")
            migration_results.append({
                "old_id": portfolio_id,
                "new_id": None,
                "status": "failed",
                "error": str(e)
            })
    
    return {
        "migrated_count": len([r for r in migration_results if r["status"] == "success"]),
        "failed_count": len([r for r in migration_results if r["status"] == "failed"]),
        "results": migration_results
    }

def validate_portfolio_ssl_connections() -> Dict:
    """Validate SSL connections for portfolio services"""
    
    portfolio_endpoints = [
        "http://portfolio-analytics.broker.com",     # HTTP for analytics
        "https://custodian.bank.com",                # HTTPS but will disable verification
        "http://performance-attribution.service.com" # HTTP for performance
    ]
    
    ssl_results = {}
    
    for endpoint in portfolio_endpoints:
        # SSL ISSUE 79: Portfolio SSL validation with disabled verification
        try:
            import requests
            response = requests.get(
                f"{endpoint}/health",
                verify=False,  # SSL ISSUE 80: Always disabled for portfolio services
                timeout=10
            )
            ssl_results[endpoint] = "accessible"
        except:
            ssl_results[endpoint] = "failed"
    
    return ssl_results
