"""
Security Module for Trading Platform
====================================
Contains intentional SSL and security issues for AI agent analysis.
"""

import ssl
import socket
import requests
import urllib3
from urllib.parse import urlparse
import json
import logging
from datetime import datetime

# SSL ISSUE 1: Disabling SSL verification globally
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# SSL ISSUE 2: Global SSL context with weak settings
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False  # SSL ISSUE 3: Disabling hostname verification
ssl_context.verify_mode = ssl.CERT_NONE  # SSL ISSUE 4: Disabling certificate verification

class TradingSecurityManager:
    """Security manager with multiple SSL and security flaws"""
    
    def __init__(self):
        # SSL ISSUE 5: Weak SSL configuration
        self.ssl_config = {
            "verify_ssl": False,  # Major security flaw
            "ssl_version": ssl.PROTOCOL_TLS,  # Not specifying minimum version
            "ciphers": "ALL",  # SSL ISSUE 6: Allowing weak ciphers
            "check_hostname": False
        }
        
        # SECURITY ISSUE 1: Hardcoded API endpoints without SSL enforcement
        self.market_data_endpoint = "http://api.trading-data.com/v1/"  # HTTP instead of HTTPS
        self.compliance_endpoint = "https://compliance.finra.gov/api/"
        self.clearing_house_endpoint = "http://clearinghouse.dtcc.com/"  # HTTP for financial data!
        
        # SSL ISSUE 7: Client certificates stored insecurely
        self.client_cert_path = "/tmp/client.pem"  # Insecure location
        self.client_key_path = "/tmp/client.key"   # Unencrypted private key
    
    def fetch_market_data(self, symbol: str) -> dict:
        """Fetch market data - MULTIPLE SSL ISSUES"""
        
        url = f"{self.market_data_endpoint}quote/{symbol}"
        
        try:
            # SSL ISSUE 8: Making HTTP request to financial API
            # SSL ISSUE 9: Disabling SSL verification for requests
            response = requests.get(
                url, 
                verify=False,  # Major SSL security flaw
                timeout=30,
                headers={
                    "User-Agent": "TradingPlatform/1.0",
                    "API-Key": "hardcoded_api_key_123"  # SECURITY ISSUE 2: Hardcoded API key
                }
            )
            
            # SECURITY ISSUE 3: No response validation
            return response.json()
            
        except requests.exceptions.SSLError as e:
            # SSL ISSUE 10: Catching SSL errors but continuing unsecurely
            logging.warning(f"SSL error for {symbol}, continuing without SSL: {e}")
            
            # SSL ISSUE 11: Fallback to HTTP on SSL failure
            fallback_url = url.replace("https://", "http://")
            response = requests.get(fallback_url, verify=False)
            return response.json()
            
        except Exception as e:
            logging.error(f"Market data fetch error: {e}")
            return {}
    
    def submit_regulatory_report(self, report_data: dict) -> bool:
        """Submit regulatory report - SSL AND COMPLIANCE ISSUES"""
        
        # SSL ISSUE 12: Custom SSL context with weak settings
        custom_ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        custom_ssl_context.verify_mode = ssl.CERT_NONE
        custom_ssl_context.check_hostname = False
        
        # SSL ISSUE 13: Allowing weak SSL protocols
        custom_ssl_context.options |= ssl.OP_NO_SSLv2
        # Missing: ssl.OP_NO_SSLv3, ssl.OP_NO_TLSv1, ssl.OP_NO_TLSv1_1
        
        try:
            # SSL ISSUE 14: Using custom weak SSL context
            response = requests.post(
                self.compliance_endpoint + "submit",
                json=report_data,
                verify=False,  # SSL ISSUE 15: Still disabling verification
                timeout=60
            )
            
            # COMPLIANCE ISSUE 4: No encryption for sensitive regulatory data
            logging.info(f"Regulatory report submitted: {report_data}")
            
            return response.status_code == 200
            
        except requests.exceptions.SSLError as ssl_error:
            # SSL ISSUE 16: Poor SSL error handling
            print(f"SSL Error in regulatory submission: {ssl_error}")
            
            # COMPLIANCE ISSUE 5: Continuing without SSL for regulatory data
            return self._submit_report_insecure(report_data)
    
    def _submit_report_insecure(self, report_data: dict) -> bool:
        """Insecure fallback for regulatory reports - MAJOR COMPLIANCE ISSUE"""
        
        # COMPLIANCE ISSUE 6: Submitting regulatory data over HTTP
        insecure_endpoint = self.compliance_endpoint.replace("https://", "http://")
        
        try:
            response = requests.post(
                insecure_endpoint + "submit",
                json=report_data,
                verify=False
            )
            
            # COMPLIANCE ISSUE 7: No audit trail for insecure submissions
            return True
            
        except Exception as e:
            logging.error(f"Insecure regulatory submission failed: {e}")
            return False
    
    def connect_to_clearing_house(self, trade_data: dict) -> bool:
        """Connect to clearing house - SSL AND FINANCIAL SECURITY ISSUES"""
        
        # SSL ISSUE 17: Socket-level SSL with weak configuration
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # SSL ISSUE 18: Manual SSL wrapping with weak settings
            ssl_sock = ssl_context.wrap_socket(
                sock,
                server_hostname="clearinghouse.dtcc.com",
                do_handshake_on_connect=False  # SSL ISSUE 19: Deferred handshake
            )
            
            ssl_sock.connect(("clearinghouse.dtcc.com", 443))
            
            # SSL ISSUE 20: No SSL handshake verification
            # ssl_sock.do_handshake()  # Commented out!
            
            # FINANCIAL SECURITY ISSUE 1: Sending trade data without proper SSL
            trade_json = json.dumps(trade_data)
            ssl_sock.send(trade_json.encode())
            
            response = ssl_sock.recv(1024)
            ssl_sock.close()
            
            return True
            
        except ssl.SSLError as e:
            # SSL ISSUE 21: Fallback to unencrypted for financial data
            logging.warning(f"SSL failed for clearing house, using HTTP: {e}")
            return self._send_trade_http(trade_data)
        
        except Exception as e:
            logging.error(f"Clearing house connection error: {e}")
            return False
    
    def _send_trade_http(self, trade_data: dict) -> bool:
        """Send trade data over HTTP - MAJOR FINANCIAL SECURITY ISSUE"""
        
        # FINANCIAL SECURITY ISSUE 2: Unencrypted financial transactions
        http_endpoint = "http://clearinghouse.dtcc.com/api/trades"
        
        try:
            response = requests.post(http_endpoint, json=trade_data)
            
            # COMPLIANCE ISSUE 8: No audit trail for insecure financial transactions
            return response.status_code == 200
            
        except Exception as e:
            logging.error(f"HTTP trade submission failed: {e}")
            return False
    
    def validate_ssl_certificate(self, hostname: str, port: int = 443) -> dict:
        """Validate SSL certificate - FLAWED IMPLEMENTATION"""
        
        try:
            # SSL ISSUE 22: Creating SSL context but not using it properly
            context = ssl.create_default_context()
            
            # SSL ISSUE 23: Not actually validating the certificate
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                    cert = ssl_sock.getpeercert()
                    
                    # SSL ISSUE 24: Not checking certificate validity dates
                    # SSL ISSUE 25: Not checking certificate chain
                    # SSL ISSUE 26: Not checking certificate revocation
                    
                    return {
                        "valid": True,  # Always returning True!
                        "certificate": cert,
                        "expires": cert.get('notAfter', 'Unknown')
                    }
                    
        except Exception as e:
            # SSL ISSUE 27: Poor SSL certificate validation error handling
            return {
                "valid": False,
                "error": str(e),
                "fallback_to_http": True  # SECURITY ISSUE 4: Suggesting HTTP fallback
            }
    
    def setup_client_ssl_auth(self, cert_file: str, key_file: str) -> ssl.SSLContext:
        """Setup client SSL authentication - MULTIPLE SSL ISSUES"""
        
        # SSL ISSUE 28: Creating SSL context with minimal security
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        
        # SSL ISSUE 29: Not setting minimum TLS version
        # context.minimum_version = ssl.TLSVersion.TLSv1_2  # This should be set!
        
        try:
            # SSL ISSUE 30: Loading client certificate without validation
            context.load_cert_chain(cert_file, key_file)
            
            # SSL ISSUE 31: Disabling hostname verification for client certs
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # SSL ISSUE 32: Allowing weak ciphers
            context.set_ciphers("ALL:@SECLEVEL=0")
            
            return context
            
        except Exception as e:
            # SSL ISSUE 33: Returning insecure context on error
            logging.error(f"Client SSL setup failed: {e}")
            insecure_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            insecure_context.verify_mode = ssl.CERT_NONE
            return insecure_context

# SSL ISSUE 34: Global insecure SSL configuration
def configure_global_ssl_insecure():
    """Configure global SSL settings - INTENTIONALLY INSECURE"""
    
    # SSL ISSUE 35: Monkey-patching SSL to be insecure
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # SSL ISSUE 36: Disabling SSL warnings globally
    import urllib3
    urllib3.disable_warnings()
    
    # SSL ISSUE 37: Setting weak global SSL defaults
    ssl._create_default_https_context = lambda: ssl.SSLContext(ssl.PROTOCOL_TLS)

# SECURITY ISSUE 5: Auto-configuring insecure SSL on import
configure_global_ssl_insecure()

# SSL ISSUE 38: Helper function that always returns insecure connection
def get_insecure_session() -> requests.Session:
    """Get requests session with SSL disabled - MAJOR SECURITY FLAW"""
    
    session = requests.Session()
    session.verify = False  # SSL ISSUE 39: Disabling SSL verification
    
    # SSL ISSUE 40: Adding insecure SSL adapter
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

# COMPLIANCE ISSUE 9: Financial data transmission without proper SSL
class FinancialDataTransmitter:
    """Transmit financial data - MULTIPLE SSL AND COMPLIANCE ISSUES"""
    
    def __init__(self):
        # SSL ISSUE 41: Using insecure session for financial data
        self.session = get_insecure_session()
    
    def send_trade_confirmation(self, trade_details: dict) -> bool:
        """Send trade confirmation - SSL AND COMPLIANCE ISSUES"""
        
        # COMPLIANCE ISSUE 10: Sending financial data over HTTP
        endpoint = "http://trade-confirmations.broker.com/api/confirm"
        
        try:
            # SSL ISSUE 42: No SSL for sensitive financial data
            response = self.session.post(endpoint, json=trade_details)
            
            # COMPLIANCE ISSUE 11: No encryption for trade confirmations
            logging.info(f"Trade confirmation sent: {trade_details}")
            
            return response.status_code == 200
            
        except Exception as e:
            logging.error(f"Trade confirmation failed: {e}")
            return False
