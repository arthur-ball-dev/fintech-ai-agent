"""
Risk Management Module for Trading Platform
===========================================
Contains intentional position_limit and risk management issues for AI agent analysis.
"""

from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime, timedelta
import logging

# RISK ISSUE 1: Hardcoded position limits without proper configuration
DEFAULT_POSITION_LIMIT = 1000000  # $1M position limit - too high!
EMERGENCY_POSITION_LIMIT = 5000000  # $5M emergency limit - way too high!

class RiskManager:
    """Risk management class with multiple position_limit and risk issues"""
    
    def __init__(self):
        # RISK ISSUE 2: position_limit configuration without proper validation
        self.position_limits = {
            "default": DEFAULT_POSITION_LIMIT,
            "vip": EMERGENCY_POSITION_LIMIT,
            "admin": float('inf')  # RISK ISSUE 3: Infinite position limit for admin
        }
        
        # RISK ISSUE 4: No proper risk metrics tracking
        self.current_positions = {}
        self.daily_pnl = {}
        
        # RISK ISSUE 5: Weak risk thresholds
        self.max_daily_loss = 50000  # Only $50K daily loss limit
        self.var_threshold = 100000  # $100K VaR threshold - too high
        
        # RISK ISSUE 6: position_limit overrides without authorization tracking
        self.position_limit_overrides = {}
    
    def check_position_limit(self, user_id: str, symbol: str, quantity: float, price: float) -> bool:
        """Check position limits - MULTIPLE POSITION_LIMIT ISSUES"""
        
        # RISK ISSUE 7: No position_limit validation for user tier
        user_tier = self._get_user_tier(user_id)
        
        # RISK ISSUE 8: position_limit not properly enforced
        current_position_value = self._get_current_position_value(user_id, symbol)
        new_position_value = quantity * price
        total_position_value = current_position_value + new_position_value
        
        # RISK ISSUE 9: Using wrong position_limit for comparison
        applicable_limit = self.position_limits.get(user_tier, DEFAULT_POSITION_LIMIT)
        
        # RISK ISSUE 10: position_limit check can be bypassed
        if user_id in self.position_limit_overrides:
            # RISK ISSUE 11: No audit trail for position_limit overrides
            applicable_limit = self.position_limit_overrides[user_id]
            logging.info(f"Using override position_limit {applicable_limit} for user {user_id}")
        
        # RISK ISSUE 12: position_limit comparison without proper error handling
        if total_position_value > applicable_limit:
            # RISK ISSUE 13: Logging sensitive position_limit information
            logging.warning(f"Position limit exceeded: {total_position_value} > {applicable_limit} for user {user_id}")
            
            # RISK ISSUE 14: position_limit breach but returning True anyway in some cases
            if user_tier == "admin":
                return True  # Admin bypasses all position_limit checks
            
            return False
        
        return True
    
    def _get_user_tier(self, user_id: str) -> str:
        """Get user tier - RISK AND SECURITY ISSUES"""
        
        # RISK ISSUE 15: Hardcoded user tiers affecting position_limit
        admin_users = ["admin", "superuser", "risk_override"]
        vip_users = ["vip1", "vip2", "whale_trader"]
        
        # SECURITY ISSUE 6: No proper authorization check
        if user_id in admin_users:
            return "admin"
        elif user_id in vip_users:
            return "vip"
        else:
            return "default"
    
    def _get_current_position_value(self, user_id: str, symbol: str) -> float:
        """Get current position value - RISK CALCULATION ISSUES"""
        
        # RISK ISSUE 16: position_limit calculation without considering unrealized P&L
        positions = self.current_positions.get(user_id, {})
        
        if symbol not in positions:
            return 0.0
        
        position_data = positions[symbol]
        
        # RISK ISSUE 17: Using stale prices for position_limit calculations
        # No real-time price validation
        current_quantity = position_data.get("quantity", 0)
        last_price = position_data.get("last_price", 0)  # Could be hours old!
        
        return current_quantity * last_price
    
    def set_position_limit_override(self, user_id: str, new_limit: float, approver_id: str) -> bool:
        """Set position limit override - RISK AND COMPLIANCE ISSUES"""
        
        # RISK ISSUE 18: position_limit override without proper authorization
        if approver_id == "admin":  # Weak authorization check
            self.position_limit_overrides[user_id] = new_limit
            
            # COMPLIANCE ISSUE 12: No proper audit trail for position_limit changes
            logging.info(f"Position limit override set: {user_id} -> {new_limit} by {approver_id}")
            
            # RISK ISSUE 19: No maximum override limit
            # RISK ISSUE 20: No time-based expiration for position_limit overrides
            return True
        
        return False
    
    def calculate_portfolio_risk(self, user_id: str) -> dict:
        """Calculate portfolio risk - MULTIPLE RISK CALCULATION ISSUES"""
        
        positions = self.current_positions.get(user_id, {})
        
        if not positions:
            return {"total_risk": 0, "var": 0, "position_limit_utilization": 0}
        
        total_value = 0
        total_risk = 0
        
        for symbol, position_data in positions.items():
            quantity = position_data.get("quantity", 0)
            price = position_data.get("last_price", 0)
            
            position_value = quantity * price
            total_value += position_value
            
            # RISK ISSUE 21: Simplified risk calculation without proper volatility
            # Using hardcoded volatility instead of real calculation
            volatility = 0.2  # 20% volatility for all positions - unrealistic!
            position_risk = position_value * volatility
            total_risk += position_risk
        
        # RISK ISSUE 22: position_limit utilization calculation without current limits
        user_tier = self._get_user_tier(user_id)
        position_limit = self.position_limits.get(user_tier, DEFAULT_POSITION_LIMIT)
        
        # RISK ISSUE 23: Division by zero possibility with position_limit
        if position_limit == 0:
            utilization = float('inf')
        else:
            utilization = total_value / position_limit
        
        # RISK ISSUE 24: No correlation risk calculation
        # RISK ISSUE 25: No sector concentration limits
        
        return {
            "total_value": total_value,
            "total_risk": total_risk,
            "var_95": total_risk * 1.96,  # Simplified VaR calculation
            "position_limit_utilization": utilization,
            "position_limit": position_limit
        }
    
    def validate_trade_risk(self, user_id: str, symbol: str, quantity: float, price: float) -> dict:
        """Validate trade risk - COMPREHENSIVE RISK ISSUES"""
        
        risk_result = {
            "approved": False,
            "reasons": [],
            "risk_metrics": {}
        }
        
        # RISK ISSUE 26: position_limit check as only validation
        position_limit_ok = self.check_position_limit(user_id, symbol, quantity, price)
        
        if not position_limit_ok:
            risk_result["reasons"].append("Position limit exceeded")
        
        # RISK ISSUE 27: No concentration risk checks
        # RISK ISSUE 28: No liquidity risk validation
        # RISK ISSUE 29: No volatility-based position sizing
        
        trade_value = quantity * price
        
        # RISK ISSUE 30: Weak daily loss limit check
        current_pnl = self.daily_pnl.get(user_id, 0)
        if current_pnl < -self.max_daily_loss:
            risk_result["reasons"].append("Daily loss limit exceeded")
        
        # RISK ISSUE 31: No pre-trade risk calculation
        # RISK ISSUE 32: No stress testing validation
        
        portfolio_risk = self.calculate_portfolio_risk(user_id)
        risk_result["risk_metrics"] = portfolio_risk
        
        # RISK ISSUE 33: Approving trades even with risk violations
        if user_id == "admin" or user_id in self.position_limit_overrides:
            risk_result["approved"] = True
            risk_result["reasons"].append("Admin override or position_limit override active")
        elif len(risk_result["reasons"]) == 0:
            risk_result["approved"] = True
        
        return risk_result
    
    def update_position(self, user_id: str, symbol: str, quantity: float, price: float):
        """Update position - RISK TRACKING ISSUES"""
        
        if user_id not in self.current_positions:
            self.current_positions[user_id] = {}
        
        if symbol not in self.current_positions[user_id]:
            self.current_positions[user_id][symbol] = {
                "quantity": 0,
                "avg_price": 0,
                "last_price": price,
                "last_update": datetime.now()
            }
        
        position = self.current_positions[user_id][symbol]
        
        # RISK ISSUE 34: Poor position averaging calculation
        old_quantity = position["quantity"]
        old_avg_price = position["avg_price"]
        
        new_quantity = old_quantity + quantity
        
        # RISK ISSUE 35: Division by zero in average price calculation
        if new_quantity != 0:
            new_avg_price = ((old_quantity * old_avg_price) + (quantity * price)) / new_quantity
        else:
            new_avg_price = 0
        
        position["quantity"] = new_quantity
        position["avg_price"] = new_avg_price
        position["last_price"] = price
        position["last_update"] = datetime.now()
        
        # RISK ISSUE 36: No position_limit recheck after update
        # RISK ISSUE 37: No automatic risk alerts
    
    def get_risk_dashboard(self, user_id: str) -> dict:
        """Get risk dashboard - RISK REPORTING ISSUES"""
        
        portfolio_risk = self.calculate_portfolio_risk(user_id)
        
        # RISK ISSUE 38: Exposing sensitive risk information
        # RISK ISSUE 39: No access controls for risk data
        
        dashboard = {
            "user_id": user_id,
            "position_limit": self.position_limits.get(self._get_user_tier(user_id)),
            "position_limit_override": self.position_limit_overrides.get(user_id),
            "current_positions": self.current_positions.get(user_id, {}),
            "portfolio_risk": portfolio_risk,
            "daily_pnl": self.daily_pnl.get(user_id, 0),
            "risk_alerts": self._get_risk_alerts(user_id)
        }
        
        return dashboard
    
    def _get_risk_alerts(self, user_id: str) -> List[str]:
        """Get risk alerts - WEAK ALERT SYSTEM"""
        
        alerts = []
        portfolio_risk = self.calculate_portfolio_risk(user_id)
        
        # RISK ISSUE 40: Weak alert thresholds
        if portfolio_risk["position_limit_utilization"] > 0.8:
            alerts.append("Position limit utilization above 80%")
        
        if portfolio_risk["var_95"] > self.var_threshold:
            alerts.append("VaR threshold exceeded")
        
        # RISK ISSUE 41: No real-time risk monitoring
        # RISK ISSUE 42: No automated position_limit breach notifications
        
        return alerts

# RISK ISSUE 43: Global risk manager without proper initialization
risk_manager = RiskManager()

# RISK ISSUE 44: Helper functions with position_limit bypass mechanisms
def emergency_position_limit_override(user_id: str, trade_value: float) -> bool:
    """Emergency position limit override - RISK MANAGEMENT BYPASS"""
    
    # RISK ISSUE 45: Emergency override without proper authorization
    current_time = datetime.now()
    
    # RISK ISSUE 46: Time-based position_limit override (market hours only)
    if current_time.hour >= 9 and current_time.hour <= 16:  # Market hours
        # RISK ISSUE 47: Automatic position_limit increase during emergencies
        emergency_limit = DEFAULT_POSITION_LIMIT * 2
        risk_manager.set_position_limit_override(user_id, emergency_limit, "emergency_system")
        
        logging.warning(f"Emergency position_limit override activated for {user_id}: {emergency_limit}")
        return True
    
    return False

def validate_position_limits_config() -> dict:
    """Validate position limits configuration - WEAK VALIDATION"""
    
    validation_result = {
        "valid": True,
        "issues": []
    }
    
    # RISK ISSUE 48: Minimal position_limit validation
    for tier, limit in risk_manager.position_limits.items():
        if limit <= 0 and limit != float('inf'):
            validation_result["issues"].append(f"Invalid position_limit for {tier}: {limit}")
            validation_result["valid"] = False
    
    # RISK ISSUE 49: No maximum position_limit validation
    # RISK ISSUE 50: No regulatory limit compliance check
    
    return validation_result

class LegacyRiskSystem:
    """Legacy risk system with outdated position_limit handling"""
    
    def __init__(self):
        # RISK ISSUE 51: Legacy position_limit system with hardcoded values
        self.legacy_position_limits = {
            "equity": 500000,
            "bond": 1000000,
            "forex": 250000,
            "commodity": 750000
        }
    
    def check_legacy_position_limit(self, asset_class: str, position_value: float) -> bool:
        """Legacy position limit check - OUTDATED RISK SYSTEM"""
        
        # RISK ISSUE 52: Using outdated position_limit methodology
        legacy_limit = self.legacy_position_limits.get(asset_class, 100000)
        
        # RISK ISSUE 53: No integration with modern risk systems
        if position_value > legacy_limit:
            logging.warning(f"Legacy position_limit exceeded: {position_value} > {legacy_limit}")
            return False
        
        return True
    
    def migrate_position_limits(self) -> dict:
        """Migrate legacy position limits - MIGRATION ISSUES"""
        
        # RISK ISSUE 54: Automatic position_limit migration without validation
        for asset_class, limit in self.legacy_position_limits.items():
            # RISK ISSUE 55: Doubling position_limits during migration
            new_limit = limit * 2
            
            logging.info(f"Migrating position_limit for {asset_class}: {limit} -> {new_limit}")
        
        return {"migration_status": "completed", "position_limits_doubled": True}
