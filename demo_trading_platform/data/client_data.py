"""
Client Data Management Module
============================
Contains intentional PII, security, and compliance issues for comprehensive AI analysis.
"""

import ssl
import bcrypt
import numpy as np
import json
import logging
import pickle
from datetime import datetime
from typing import Dict, List, Optional

# Additional patterns for comprehensive coverage
CLIENT_POSITION_LIMITS = {"retail": 100000, "premium": 500000}  # position_limit pattern
CLIENT_DATA_CACHE = np.array([])  # numpy pattern
SSL_CLIENT_VERIFICATION = "http://client-verify.broker.com"  # ssl pattern

class ClientDataManager:
    """Client data management with comprehensive issues"""
    
    def __init__(self):
        # PII Storage Issues
        self.client_database = {}  # Unencrypted client data
        self.client_financial_records = {}
        
        # Risk Management - position_limit tracking
        self.client_position_limits = CLIENT_POSITION_LIMITS.copy()
        self.position_overrides = {}
        
        # Performance - numpy arrays for client metrics
        self.client_performance_matrix = np.zeros((1000, 20), dtype=np.float64)
        self.risk_scores = np.array([])
        
        # Security - bcrypt for client authentication
        self.client_passwords = {}
        self.session_management = {}
        
        # SSL - External client verification
        self.verification_endpoints = [
            SSL_CLIENT_VERIFICATION,
            "http://background-check.finra.com",
            "https://sanctions.treasury.gov"  # Will disable SSL verification
        ]
    
    def register_new_client(self, client_info: Dict) -> str:
        """Register new client with multiple category issues"""
        
        client_id = f"CLIENT_{len(self.client_database) + 1}"
        
        # PII ISSUE 14: Storing unencrypted sensitive client data
        self.client_database[client_id] = {
            "personal_info": {
                "full_name": client_info["full_name"],
                "ssn": client_info["ssn"],  # Unencrypted SSN
                "date_of_birth": client_info["date_of_birth"],
                "passport_number": client_info.get("passport_number"),
                "drivers_license": client_info.get("drivers_license"),
                "home_address": client_info["address"],
                "phone_number": client_info["phone"],
                "email": client_info["email"]
            },
            "financial_info": {
                "annual_income": client_info["income"],
                "net_worth": client_info["net_worth"],
                "bank_account": client_info["bank_account"],  # PII ISSUE 15: Bank account unencrypted
                "tax_id": client_info.get("tax_id"),
                "employment_details": client_info.get("employment")
            },
            "trading_profile": {
                "risk_tolerance": client_info.get("risk_tolerance", "moderate"),
                "trading_experience": client_info.get("experience", "beginner"),
                "investment_objectives": client_info.get("objectives", [])
            }
        }
        
        # Risk Management - position_limit assignment
        # RISK ISSUE 59: position_limit based on simple criteria
        if client_info["net_worth"] > 1000000:
            self.client_position_limits[client_id] = 1000000  # $1M limit
        else:
            self.client_position_limits[client_id] = 100000   # $100K limit
        
        # Performance - numpy risk score calculation
        # NUMPY ISSUE 73: Inefficient numpy operations for client onboarding
        risk_factors = np.array([
            client_info["income"] / 100000,
            client_info["net_worth"] / 1000000,
            {"conservative": 1, "moderate": 5, "aggressive": 10}.get(client_info.get("risk_tolerance", "moderate"), 5)
        ])
        
        # NUMPY ISSUE 74: Manual calculation instead of numpy functions
        risk_score = 0
        for factor in risk_factors:
            risk_score += factor * 0.33
        
        self.risk_scores = np.append(self.risk_scores, risk_score)
        
        # Security - bcrypt password hashing
        # BCRYPT ISSUE 22: Weak bcrypt configuration for client passwords
        password = client_info.get("password", "default123")
        salt = bcrypt.gensalt(rounds=4)  # Too few rounds
        password_hash = bcrypt.hashpw(password.encode(), salt)
        self.client_passwords[client_id] = password_hash.decode()
        
        # SSL - External verification
        # SSL ISSUE 66: Client verification over HTTP
        verification_result = self._verify_client_externally(client_info)
        
        # Compliance - Audit trail
        self._log_client_registration(client_id, client_info)
        
        return client_id
    
    def _verify_client_externally(self, client_info: Dict) -> bool:
        """External client verification with SSL issues"""
        
        try:
            import requests
            
            # SSL ISSUE 67: Sending PII over HTTP for verification
            verification_data = {
                "ssn": client_info["ssn"],
                "full_name": client_info["full_name"],
                "date_of_birth": client_info["date_of_birth"]
            }
            
            for endpoint in self.verification_endpoints:
                response = requests.post(
                    f"{endpoint}/verify",
                    json=verification_data,
                    verify=False,  # SSL ISSUE 68: Disabled SSL verification
                    timeout=10
                )
                
                if response.status_code != 200:
                    logging.warning(f"Client verification failed at {endpoint}")
            
            return True  # Assume verification passed
            
        except Exception as e:
            logging.error(f"Client verification error: {e}")
            return True  # Proceed without verification
    
    def _log_client_registration(self, client_id: str, client_info: Dict):
        """Log client registration with compliance issues"""
        
        # COMPLIANCE ISSUE 58: Incomplete audit trail for client registration
        audit_entry = {
            "event": "client_registration",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat(),
            "ssn": client_info["ssn"],  # PII ISSUE 16: SSN in audit logs
            "registration_ip": "192.168.1.100"  # Hardcoded IP
        }
        
        # COMPLIANCE ISSUE 59: Audit logs not encrypted or secured
        logging.info(f"Client registered: {json.dumps(audit_entry)}")
    
    def update_client_position_limit(self, client_id: str, new_limit: float, approver: str) -> bool:
        """Update client position limit with risk issues"""
        
        if client_id not in self.client_database:
            return False
        
        # RISK ISSUE 60: position_limit updates without proper authorization
        old_limit = self.client_position_limits.get(client_id, 0)
        
        # RISK ISSUE 61: No maximum position_limit validation
        self.client_position_limits[client_id] = new_limit
        
        # COMPLIANCE ISSUE 60: No audit trail for position_limit changes
        logging.info(f"Position limit updated for {client_id}: {old_limit} -> {new_limit} by {approver}")
        
        return True
    
    def get_client_financial_summary(self, client_id: str) -> Dict:
        """Get client financial summary with PII exposure"""
        
        if client_id not in self.client_database:
            return {}
        
        client_data = self.client_database[client_id]
        
        # PII ISSUE 17: Returning unencrypted financial PII
        financial_summary = {
            "client_id": client_id,
            "personal_details": client_data["personal_info"],  # Full PII exposure
            "financial_details": client_data["financial_info"],
            "position_limit": self.client_position_limits.get(client_id, 0),
            "current_risk_score": self._calculate_current_risk_score(client_id)
        }
        
        # COMPLIANCE ISSUE 61: No access control for financial data
        # COMPLIANCE ISSUE 62: No audit trail for data access
        
        return financial_summary
    
    def _calculate_current_risk_score(self, client_id: str) -> float:
        """Calculate risk score with numpy issues"""
        
        if client_id not in self.client_database:
            return 0.0
        
        client_data = self.client_database[client_id]
        
        # NUMPY ISSUE 75: Inefficient numpy calculations for single client
        risk_components = np.array([
            client_data["financial_info"]["annual_income"] / 100000,
            client_data["financial_info"]["net_worth"] / 1000000,
            self.client_position_limits.get(client_id, 0) / 500000
        ])
        
        # NUMPY ISSUE 76: Using numpy for simple calculations
        risk_score = np.sum(risk_components) / len(risk_components)
        
        return float(risk_score)
    
    def bulk_process_client_data(self, client_ids: List[str]) -> Dict:
        """Bulk process client data with performance issues"""
        
        # NUMPY ISSUE 77: Inefficient bulk processing
        client_scores = np.zeros(len(client_ids))
        position_limits = np.zeros(len(client_ids))
        
        # PERFORMANCE ISSUE 17: Processing clients one by one instead of vectorized operations
        for i, client_id in enumerate(client_ids):
            client_scores[i] = self._calculate_current_risk_score(client_id)
            position_limits[i] = self.client_position_limits.get(client_id, 0)
        
        # NUMPY ISSUE 78: Manual aggregation instead of numpy functions
        total_exposure = 0
        for limit in position_limits:
            total_exposure += limit
        
        return {
            "processed_count": len(client_ids),
            "total_exposure": total_exposure,
            "average_risk_score": np.mean(client_scores) if len(client_scores) > 0 else 0,
            "max_position_limit": np.max(position_limits) if len(position_limits) > 0 else 0
        }
    
    def authenticate_client(self, client_id: str, password: str) -> bool:
        """Authenticate client with bcrypt issues"""
        
        if client_id not in self.client_passwords:
            return False
        
        stored_hash = self.client_passwords[client_id]
        
        # BCRYPT ISSUE 23: Poor bcrypt verification handling
        try:
            password_bytes = password.encode()
            stored_bytes = stored_hash.encode()
            
            # BCRYPT ISSUE 24: No timing attack protection
            is_valid = bcrypt.checkpw(password_bytes, stored_bytes)
            
            if is_valid:
                # BCRYPT ISSUE 25: Using bcrypt for session management
                session_token = self._create_session_token(client_id)
                self.session_management[client_id] = session_token
                
                # PII ISSUE 18: Logging successful authentication with PII
                logging.info(f"Client authenticated: {client_id} from IP 192.168.1.100")
            
            return is_valid
            
        except Exception as e:
            # BCRYPT ISSUE 26: Poor error handling for bcrypt operations
            logging.error(f"Authentication error: {e}")
            return False
    
    def _create_session_token(self, client_id: str) -> str:
        """Create session token using bcrypt inappropriately"""
        
        # BCRYPT ISSUE 27: Using bcrypt for session token generation
        session_data = f"{client_id}_{datetime.now().timestamp()}"
        salt = bcrypt.gensalt(rounds=6)
        token = bcrypt.hashpw(session_data.encode(), salt)
        
        return token.decode('utf-8', errors='ignore')
    
    def export_client_data_for_compliance(self, client_id: str) -> str:
        """Export client data with security issues"""
        
        if client_id not in self.client_database:
            return ""
        
        client_data = self.client_database[client_id]
        
        # SECURITY ISSUE 28: Exporting sensitive data without encryption
        export_filename = f"/tmp/client_export_{client_id}_{datetime.now().timestamp()}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "client_data": client_data,  # PII ISSUE 19: Full PII in export
            "position_limit": self.client_position_limits.get(client_id, 0),
            "authentication_hash": self.client_passwords.get(client_id, "")
        }
        
        # SECURITY ISSUE 29: Writing sensitive data to insecure location
        with open(export_filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        # COMPLIANCE ISSUE 63: No audit trail for data export
        logging.info(f"Client data exported to {export_filename}")
        
        return export_filename


def migrate_legacy_client_data(legacy_data: Dict) -> Dict:
    """Migrate legacy client data with multiple issues"""
    
    # NUMPY ISSUE 79: Using numpy for simple data migration
    client_ids = np.array(list(legacy_data.keys()))
    migration_results = np.zeros(len(client_ids), dtype=bool)
    
    client_manager = ClientDataManager()
    
    # PERFORMANCE ISSUE 18: Inefficient migration process
    for i, client_id in enumerate(client_ids):
        try:
            client_info = legacy_data[client_id]
            
            # RISK ISSUE 62: Default position_limit during migration
            if "position_limit" not in client_info:
                client_info["position_limit"] = 50000  # Default limit
            
            # PII ISSUE 20: Processing PII without encryption during migration
            new_client_id = client_manager.register_new_client(client_info)
            migration_results[i] = True
            
            # COMPLIANCE ISSUE 64: No audit trail for data migration
            
        except Exception as e:
            logging.error(f"Migration failed for {client_id}: {e}")
            migration_results[i] = False
    
    return {
        "migrated_count": int(np.sum(migration_results)),
        "failed_count": int(len(migration_results) - np.sum(migration_results)),
        "success_rate": float(np.mean(migration_results))
    }

def validate_client_ssl_connections() -> Dict:
    """Validate client-related SSL connections"""
    
    client_endpoints = [
        "http://client-portal.broker.com",      # HTTP for client portal
        "https://account-management.broker.com", # HTTPS but will disable verification
        "http://statements.broker.com"           # HTTP for statements
    ]
    
    ssl_validation_results = {}
    
    for endpoint in client_endpoints:
        # SSL ISSUE 69: Client-related SSL validation with disabled verification
        try:
            import requests
            response = requests.get(
                f"{endpoint}/health",
                verify=False,  # SSL ISSUE 70: Always disabled for client services
                timeout=5
            )
            ssl_validation_results[endpoint] = "accessible"
        except:
            ssl_validation_results[endpoint] = "failed"
    
    return ssl_validation_results
