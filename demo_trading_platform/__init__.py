"""
Fake Trading Platform Package
============================
A deliberately flawed trading platform for AI agent analysis and testing.

This package contains intentional security, compliance, performance, and architectural
issues across multiple categories to provide comprehensive testing coverage for
FinTech AI agents.

IMPORTANT: This is a fake trading platform with intentional flaws.
DO NOT USE IN PRODUCTION.

Categories of Issues Included:
- Risk Management: position_limit violations and weak risk controls
- Performance: numpy inefficiencies and poor algorithm design  
- Compliance: SSL/TLS issues and insecure communications
- Architecture: FastAPI misuse and poor design patterns
- Security: bcrypt misuse and authentication weaknesses
- PII Handling: Unencrypted sensitive data and privacy violations
"""

# Import main components to trigger pattern detection
from .main import app
from .auth.authentication import auth_manager
from .auth.security import TradingSecurityManager
from .trading.risk_management import risk_manager
from .trading.order_engine import OrderEngine
from .analytics.performance import PerformanceAnalyzer
from .compliance.audit import compliance_manager
from .data.client_data import ClientDataManager

# Package metadata
__version__ = "1.0.0-insecure"
__author__ = "Fake Trading Platform (Intentionally Flawed)"
__description__ = "A deliberately flawed trading platform for AI agent testing"

# Global instances with intentional issues
GLOBAL_RISK_MANAGER = risk_manager
GLOBAL_COMPLIANCE_MANAGER = compliance_manager
GLOBAL_SECURITY_MANAGER = TradingSecurityManager()
GLOBAL_ORDER_ENGINE = OrderEngine()
GLOBAL_PERFORMANCE_ANALYZER = PerformanceAnalyzer()
GLOBAL_CLIENT_MANAGER = ClientDataManager()

# Configuration with intentional security issues
TRADING_CONFIG = {
    "ssl_verify": False,  # SSL ISSUE 71: Global SSL verification disabled
    "debug_mode": True,   # SECURITY ISSUE 30: Debug mode in production
    "log_level": "DEBUG", # SECURITY ISSUE 31: Verbose logging
    "default_position_limit": 1000000,  # RISK ISSUE 63: High default position limit
    "bcrypt_rounds": 4,   # BCRYPT ISSUE 28: Weak bcrypt configuration
    "numpy_warnings": "ignore"  # NUMPY ISSUE 80: Suppressing numpy warnings
}

def initialize_trading_platform():
    """Initialize the trading platform with flawed configurations"""
    
    # SSL ISSUE 72: Configuring global SSL to be insecure
    import ssl
    import urllib3
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # NUMPY ISSUE 81: Global numpy configuration with issues
    import numpy as np
    np.seterr(all='ignore')  # Ignoring all numpy errors globally
    
    # BCRYPT ISSUE 29: Global bcrypt configuration
    import bcrypt
    # Setting weak global bcrypt rounds (conceptually)
    
    # RISK ISSUE 64: Initializing risk management with weak defaults
    GLOBAL_RISK_MANAGER.position_limits["emergency"] = float('inf')
    
    # COMPLIANCE ISSUE 65: Weak compliance initialization
    GLOBAL_COMPLIANCE_MANAGER.ssl_verify_regulatory = False
    
    print("⚠️  Fake Trading Platform Initialized with Intentional Security Flaws ⚠️")
    print("This platform contains deliberate vulnerabilities for AI agent testing.")
    print("Categories: position_limit, numpy, ssl, fastapi, bcrypt, PII, compliance")

def get_platform_status():
    """Get platform status showing various issues"""
    
    return {
        "platform": "Fake Trading Platform",
        "version": __version__,
        "status": "running_with_vulnerabilities",
        "issues": {
            "ssl_verification": "disabled",
            "position_limits": "inadequate", 
            "numpy_warnings": "suppressed",
            "bcrypt_strength": "weak",
            "compliance_mode": "non_compliant",
            "pii_protection": "disabled",
            "audit_trail": "incomplete"
        },
        "components": {
            "risk_manager": "initialized_with_flaws",
            "order_engine": "performance_issues",
            "compliance_manager": "ssl_disabled",
            "client_manager": "pii_exposed",
            "performance_analyzer": "numpy_inefficient"
        }
    }

# Auto-initialize with flawed configuration
initialize_trading_platform()

# Export components for easy access
__all__ = [
    'app',
    'auth_manager', 
    'risk_manager',
    'compliance_manager',
    'GLOBAL_RISK_MANAGER',
    'GLOBAL_COMPLIANCE_MANAGER',
    'GLOBAL_SECURITY_MANAGER',
    'GLOBAL_ORDER_ENGINE',
    'GLOBAL_PERFORMANCE_ANALYZER', 
    'GLOBAL_CLIENT_MANAGER',
    'TRADING_CONFIG',
    'initialize_trading_platform',
    'get_platform_status'
]
