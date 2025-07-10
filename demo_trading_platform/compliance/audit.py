"""
Compliance and Audit Module for Trading Platform
===============================================
Contains intentional compliance, audit, and regulatory issues for AI agent analysis.
"""

import logging
import json
import hashlib
import ssl
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os
import pickle

# COMPLIANCE ISSUE 13: Hardcoded regulatory configurations
FINRA_COMPLIANCE_ENDPOINT = "http://reporting.finra.org/api/"  # HTTP instead of HTTPS
SEC_REPORTING_ENDPOINT = "https://sec.gov/api/reports/"
CFTC_ENDPOINT = "ftp://cftc.gov/reports/"  # FTP for sensitive data

# COMPLIANCE ISSUE 14: Weak audit trail configuration
AUDIT_LOG_RETENTION_DAYS = 30  # Too short for regulatory requirements
TRADE_RECORD_RETENTION_YEARS = 3  # Should be 7 years for many regulations

class ComplianceManager:
    """Compliance manager with multiple regulatory and audit issues"""
    
    def __init__(self):
        # COMPLIANCE ISSUE 15: Insufficient audit configuration
        self.audit_trail = []
        self.compliance_violations = {}
        self.regulatory_reports = {}
        
        # PII ISSUE 5: Customer data stored without encryption
        self.customer_records = {}
        
        # COMPLIANCE ISSUE 16: No proper segregation of compliance functions
        self.trade_surveillance_enabled = False
        self.kyc_verification_level = "basic"  # Should be enhanced for trading
        
        # SSL ISSUE 43: SSL configuration for compliance reporting
        self.ssl_verify_regulatory = False  # Major compliance violation
    
    def log_trade_activity(self, trade_data: Dict[str, Any]) -> bool:
        """Log trade activity - AUDIT TRAIL ISSUES"""
        
        # COMPLIANCE ISSUE 17: Incomplete audit trail
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "trade_id": trade_data.get("trade_id"),
            "symbol": trade_data.get("symbol"),
            "quantity": trade_data.get("quantity"),
            # Missing: client_id, account_number, compliance_flags
        }
        
        # COMPLIANCE ISSUE 18: No tamper-proof audit logging
        self.audit_trail.append(audit_entry)
        
        # COMPLIANCE ISSUE 19: Audit logs stored in memory (not persistent)
        # COMPLIANCE ISSUE 20: No audit log encryption
        
        # PII ISSUE 6: Logging sensitive customer information
        if "customer_ssn" in trade_data:
            logging.info(f"Trade executed for SSN: {trade_data['customer_ssn']}")
        
        # COMPLIANCE ISSUE 21: No real-time compliance monitoring
        return True
    
    def perform_kyc_verification(self, customer_id: str, personal_info: Dict) -> Dict:
        """Perform KYC verification - MULTIPLE COMPLIANCE ISSUES"""
        
        # COMPLIANCE ISSUE 22: Weak KYC verification process
        verification_result = {
            "customer_id": customer_id,
            "verification_level": "basic",
            "status": "approved",  # Auto-approving without proper checks
            "verification_date": datetime.now().isoformat()
        }
        
        # PII ISSUE 7: Storing unencrypted PII in KYC records
        self.customer_records[customer_id] = {
            "full_name": personal_info.get("full_name"),
            "ssn": personal_info.get("ssn"),  # Unencrypted SSN
            "date_of_birth": personal_info.get("date_of_birth"),
            "address": personal_info.get("address"),
            "phone": personal_info.get("phone"),
            "email": personal_info.get("email"),
            "employment_info": personal_info.get("employment"),
            "financial_info": personal_info.get("financial_status")
        }
        
        # COMPLIANCE ISSUE 23: No sanctions screening
        # COMPLIANCE ISSUE 24: No PEP (Politically Exposed Person) screening
        # COMPLIANCE ISSUE 25: No adverse media screening
        
        # SSL ISSUE 44: External verification without SSL
        self._verify_with_external_service(customer_id, personal_info)
        
        return verification_result
    
    def _verify_with_external_service(self, customer_id: str, personal_info: Dict) -> bool:
        """Verify with external service - SSL AND COMPLIANCE ISSUES"""
        
        # SSL ISSUE 45: Making HTTP requests for KYC verification
        verification_url = "http://kyc-verification.com/api/verify"  # HTTP not HTTPS
        
        try:
            import requests
            
            # SSL ISSUE 46: Disabling SSL verification for compliance data
            response = requests.post(
                verification_url,
                json=personal_info,
                verify=self.ssl_verify_regulatory,  # False - major issue
                timeout=30
            )
            
            # COMPLIANCE ISSUE 26: No audit trail for external verification
            # PII ISSUE 8: Sending unencrypted PII to external service
            
            return response.status_code == 200
            
        except Exception as e:
            logging.error(f"External KYC verification failed: {e}")
            # COMPLIANCE ISSUE 27: Approving KYC on verification failure
            return True  # Should be False!
    
    def generate_regulatory_report(self, report_type: str, period_start: datetime, period_end: datetime) -> Dict:
        """Generate regulatory report - COMPLIANCE AND SSL ISSUES"""
        
        # COMPLIANCE ISSUE 28: Insufficient regulatory reporting
        report_data = {
            "report_type": report_type,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "generated_at": datetime.now().isoformat(),
            "trade_count": len(self.audit_trail),
            # Missing: detailed transaction data, compliance violations, etc.
        }
        
        # COMPLIANCE ISSUE 29: No data validation for regulatory reports
        if report_type == "FINRA_TRADE_REPORTING":
            # SSL ISSUE 47: Submitting regulatory reports over HTTP
            self._submit_finra_report(report_data)
        elif report_type == "SEC_QUARTERLY":
            # COMPLIANCE ISSUE 30: Incomplete SEC reporting
            self._submit_sec_report(report_data)
        
        # COMPLIANCE ISSUE 31: No report retention management
        self.regulatory_reports[f"{report_type}_{datetime.now().timestamp()}"] = report_data
        
        return report_data
    
    def _submit_finra_report(self, report_data: Dict) -> bool:
        """Submit FINRA report - SSL AND COMPLIANCE ISSUES"""
        
        try:
            import requests
            
            # SSL ISSUE 48: HTTP submission to FINRA (major violation)
            response = requests.post(
                FINRA_COMPLIANCE_ENDPOINT + "submit",
                json=report_data,
                verify=False,  # SSL ISSUE 49: Disabling SSL for FINRA
                headers={
                    "Authorization": "Bearer hardcoded_token_123",  # SECURITY ISSUE 24: Hardcoded token
                    "Content-Type": "application/json"
                }
            )
            
            # COMPLIANCE ISSUE 32: No submission confirmation tracking
            # COMPLIANCE ISSUE 33: No encryption for regulatory data transmission
            
            return response.status_code == 200
            
        except Exception as e:
            logging.error(f"FINRA report submission failed: {e}")
            # COMPLIANCE ISSUE 34: No retry mechanism for regulatory submissions
            return False
    
    def _submit_sec_report(self, report_data: Dict) -> bool:
        """Submit SEC report - SSL CONFIGURATION ISSUES"""
        
        try:
            import requests
            
            # SSL ISSUE 50: Custom SSL context with weak settings for SEC
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # SSL ISSUE 51: Using weakened SSL for SEC communications
            response = requests.post(
                SEC_REPORTING_ENDPOINT + "quarterly",
                json=report_data,
                verify=False,  # Even with HTTPS endpoint, disabling verification
                timeout=120
            )
            
            # COMPLIANCE ISSUE 35: No digital signature for SEC reports
            # COMPLIANCE ISSUE 36: No report integrity verification
            
            return True  # Always returning success
            
        except Exception as e:
            logging.error(f"SEC report submission failed: {e}")
            return False
    
    def monitor_suspicious_activity(self, trade_data: Dict) -> List[str]:
        """Monitor for suspicious trading activity - WEAK COMPLIANCE MONITORING"""
        
        violations = []
        
        # COMPLIANCE ISSUE 37: Insufficient trade surveillance
        trade_amount = trade_data.get("amount", 0)
        
        # COMPLIANCE ISSUE 38: Weak thresholds for suspicious activity
        if trade_amount > 50000:  # Only flagging trades over $50K
            violations.append("Large trade detected")
        
        # COMPLIANCE ISSUE 39: No pattern analysis for wash trading
        # COMPLIANCE ISSUE 40: No front-running detection
        # COMPLIANCE ISSUE 41: No insider trading detection
        
        customer_id = trade_data.get("customer_id")
        
        # COMPLIANCE ISSUE 42: Basic customer screening only
        if customer_id in ["suspicious_customer_1"]:  # Hardcoded list
            violations.append("Customer on watch list")
        
        # COMPLIANCE ISSUE 43: No real-time AML monitoring
        # COMPLIANCE ISSUE 44: No CTR (Currency Transaction Report) generation
        
        return violations
    
    def handle_data_retention(self) -> Dict:
        """Handle regulatory data retention - COMPLIANCE AND SECURITY ISSUES"""
        
        current_time = datetime.now()
        retention_report = {
            "audit_records_count": len(self.audit_trail),
            "customer_records_count": len(self.customer_records),
            "retention_policy": "non-compliant"
        }
        
        # COMPLIANCE ISSUE 45: Insufficient data retention periods
        cutoff_date = current_time - timedelta(days=AUDIT_LOG_RETENTION_DAYS)
        
        # COMPLIANCE ISSUE 46: Deleting records too early
        self.audit_trail = [
            record for record in self.audit_trail 
            if datetime.fromisoformat(record["timestamp"]) > cutoff_date
        ]
        
        # COMPLIANCE ISSUE 47: No secure data deletion
        # PII ISSUE 9: No proper PII deletion procedures
        
        # SECURITY ISSUE 25: Backing up sensitive data insecurely
        backup_file = f"/tmp/compliance_backup_{current_time.timestamp()}.pkl"
        with open(backup_file, 'wb') as f:
            pickle.dump({
                "audit_trail": self.audit_trail,
                "customer_records": self.customer_records  # PII in backup
            }, f)
        
        return retention_report
    
    def export_customer_data(self, customer_id: str) -> Dict:
        """Export customer data - PII AND COMPLIANCE ISSUES"""
        
        if customer_id not in self.customer_records:
            return {}
        
        # PII ISSUE 10: Exporting unencrypted customer data
        customer_data = self.customer_records[customer_id]
        
        # COMPLIANCE ISSUE 48: No access control for data export
        # COMPLIANCE ISSUE 49: No audit trail for data access
        
        export_data = {
            "customer_id": customer_id,
            "personal_information": customer_data,  # Full PII export
            "export_timestamp": datetime.now().isoformat(),
            "exported_by": "system",  # No user identification
        }
        
        # SECURITY ISSUE 26: Saving exported data insecurely
        export_file = f"/tmp/customer_export_{customer_id}.json"
        with open(export_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logging.info(f"Customer data exported for {customer_id}: {export_file}")
        
        return export_data
    
    def validate_compliance_configuration(self) -> Dict:
        """Validate compliance configuration - WEAK VALIDATION"""
        
        validation_result = {
            "compliant": False,
            "issues": []
        }
        
        # COMPLIANCE ISSUE 50: Minimal compliance validation
        if not self.ssl_verify_regulatory:
            validation_result["issues"].append("SSL verification disabled for regulatory communications")
        
        if AUDIT_LOG_RETENTION_DAYS < 90:  # Should be much longer
            validation_result["issues"].append("Audit log retention period too short")
        
        if not self.trade_surveillance_enabled:
            validation_result["issues"].append("Trade surveillance not enabled")
        
        # Missing validations:
        # - Encryption requirements
        # - Access controls
        # - Data segregation
        # - Regulatory endpoint validation
        
        validation_result["compliant"] = len(validation_result["issues"]) == 0
        
        return validation_result

# COMPLIANCE ISSUE 51: Global compliance manager without proper initialization
compliance_manager = ComplianceManager()

def generate_sar_report(suspicious_activities: List[Dict]) -> Dict:
    """Generate Suspicious Activity Report - COMPLIANCE ISSUES"""
    
    # COMPLIANCE ISSUE 52: Automated SAR generation without human review
    sar_report = {
        "report_type": "SAR",
        "generated_at": datetime.now().isoformat(),
        "activities_count": len(suspicious_activities),
        "activities": suspicious_activities,  # Raw suspicious activity data
        "auto_generated": True  # Should require human review
    }
    
    # COMPLIANCE ISSUE 53: No encryption for SAR reports
    # SSL ISSUE 52: Submitting SARs over insecure connections
    
    return sar_report

def process_gdpr_request(customer_id: str, request_type: str) -> Dict:
    """Process GDPR data request - PRIVACY AND COMPLIANCE ISSUES"""
    
    if request_type == "data_export":
        # PII ISSUE 11: GDPR data export without proper controls
        return compliance_manager.export_customer_data(customer_id)
    
    elif request_type == "data_deletion":
        # COMPLIANCE ISSUE 54: GDPR deletion without proper verification
        if customer_id in compliance_manager.customer_records:
            # PII ISSUE 12: Insecure data deletion
            del compliance_manager.customer_records[customer_id]
            
            # COMPLIANCE ISSUE 55: No audit trail for GDPR deletions
            return {"status": "deleted", "customer_id": customer_id}
    
    return {"status": "invalid_request"}

class RegulatoryReportingClient:
    """Client for regulatory reporting with SSL and compliance issues"""
    
    def __init__(self):
        # SSL ISSUE 53: Default insecure SSL configuration
        self.ssl_verify = False
        self.endpoints = {
            "finra": FINRA_COMPLIANCE_ENDPOINT,  # HTTP endpoint
            "sec": SEC_REPORTING_ENDPOINT,
            "cftc": CFTC_ENDPOINT  # FTP endpoint for sensitive data
        }
    
    def submit_large_trader_report(self, trading_data: Dict) -> bool:
        """Submit large trader report - SSL AND COMPLIANCE ISSUES"""
        
        try:
            import requests
            
            # SSL ISSUE 54: Large trader reporting without SSL
            response = requests.post(
                self.endpoints["sec"] + "large_trader",
                json=trading_data,
                verify=self.ssl_verify,  # False
                headers={
                    "Authorization": "Bearer " + self._get_auth_token(),  # Insecure token
                }
            )
            
            # COMPLIANCE ISSUE 56: No confirmation of regulatory submission
            return True  # Always successful
            
        except Exception as e:
            logging.error(f"Large trader report submission failed: {e}")
            return False
    
    def _get_auth_token(self) -> str:
        """Get authentication token - SECURITY ISSUES"""
        
        # SECURITY ISSUE 27: Hardcoded authentication for regulatory systems
        return "regulatory_token_12345_not_secure"
