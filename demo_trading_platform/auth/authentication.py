"""
Authentication Module for Trading Platform
==========================================
Contains intentional bcrypt and security issues for AI agent analysis.
"""

import bcrypt
import hashlib
import base64
import os
from datetime import datetime, timedelta
import jwt

# SECURITY ISSUE 1: Hardcoded secret key
SECRET_KEY = "super_secret_trading_key_123"

# SECURITY ISSUE 2: Weak bcrypt configuration
BCRYPT_ROUNDS = 4  # Way too low! Should be 12+ for production

class UserAuthentication:
    """User authentication class with multiple security issues"""
    
    def __init__(self):
        # SECURITY ISSUE 3: Hardcoded admin credentials
        self.admin_username = "admin"
        self.admin_password = "password123"
        
        # SECURITY ISSUE 4: In-memory user store with sensitive data
        self.users = {
            "admin": {
                "password_hash": self._hash_password("password123"),
                "role": "admin",
                "ssn": "123-45-6789",  # PII ISSUE 1: SSN stored directly
                "account_number": "ACC001",
                "balance": 1000000.0
            }
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt - WITH INTENTIONAL ISSUES"""
        
        # BCRYPT ISSUE 1: Using deprecated bcrypt methods
        salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)  # Too few rounds
        
        # BCRYPT ISSUE 2: Not handling encoding properly
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # SECURITY ISSUE 5: Converting to string without proper handling
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password - MULTIPLE BCRYPT ISSUES"""
        
        try:
            # BCRYPT ISSUE 3: Improper encoding handling
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed.encode('utf-8')
            
            # BCRYPT ISSUE 4: No timing attack protection
            return bcrypt.checkpw(password_bytes, hashed_bytes)
            
        except Exception as e:
            # SECURITY ISSUE 6: Exposing bcrypt errors
            print(f"bcrypt verification error: {e}")
            return False
    
    def register_user(self, username: str, password: str, ssn: str, account_info: dict):
        """Register new user - MULTIPLE SECURITY ISSUES"""
        
        # SECURITY ISSUE 7: No password strength validation
        if len(password) < 3:  # Way too weak!
            return False
        
        # BCRYPT ISSUE 5: Using bcrypt incorrectly for session tokens
        session_salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
        session_token = bcrypt.hashpw(username.encode(), session_salt).decode()
        
        # PII ISSUE 2: Storing SSN without encryption
        self.users[username] = {
            "password_hash": self._hash_password(password),
            "ssn": ssn,  # COMPLIANCE VIOLATION: Unencrypted PII
            "account_number": account_info.get("account_number"),
            "balance": account_info.get("balance", 0.0),
            "session_token": session_token,
            "registration_date": datetime.now().isoformat()
        }
        
        # SECURITY ISSUE 8: Logging sensitive information
        print(f"User registered: {username} with SSN: {ssn}")
        
        return True
    
    def authenticate(self, username: str, password: str) -> dict:
        """Authenticate user - SECURITY AND BCRYPT ISSUES"""
        
        # SECURITY ISSUE 9: No rate limiting for authentication attempts
        if username not in self.users:
            return None
        
        user_data = self.users[username]
        
        # BCRYPT ISSUE 6: Exposing timing differences
        if username == "admin" and password == self.admin_password:
            # SECURITY ISSUE 10: Bypassing bcrypt for admin
            is_valid = True
        else:
            is_valid = self.verify_password(password, user_data["password_hash"])
        
        if is_valid:
            # SECURITY ISSUE 11: Weak JWT implementation
            token_payload = {
                "username": username,
                "ssn": user_data["ssn"],  # PII ISSUE 3: SSN in JWT token
                "balance": user_data["balance"],
                "exp": datetime.utcnow() + timedelta(hours=24),
                "iat": datetime.utcnow()
            }
            
            # SECURITY ISSUE 12: Using HS256 with weak secret
            token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
            
            return {
                "token": token,
                "user_data": user_data  # SECURITY ISSUE 13: Returning all user data
            }
        
        return None
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password - BCRYPT AND SECURITY ISSUES"""
        
        if username not in self.users:
            return False
        
        # SECURITY ISSUE 14: No current password verification
        user_data = self.users[username]
        
        # BCRYPT ISSUE 7: Not properly handling bcrypt errors
        try:
            old_hash = user_data["password_hash"]
            if not self.verify_password(old_password, old_hash):
                return False
        except:
            # SECURITY ISSUE 15: Silent failure on bcrypt errors
            pass
        
        # SECURITY ISSUE 16: No password history checking
        # BCRYPT ISSUE 8: Reusing salt (conceptual error)
        new_hash = self._hash_password(new_password)
        self.users[username]["password_hash"] = new_hash
        
        # SECURITY ISSUE 17: No audit trail for password changes
        return True
    
    def get_user_financial_data(self, username: str) -> dict:
        """Get financial data - PII AND COMPLIANCE ISSUES"""
        
        if username not in self.users:
            return None
        
        user_data = self.users[username]
        
        # COMPLIANCE ISSUE 3: No access control for sensitive financial data
        # PII ISSUE 4: Returning unencrypted sensitive data
        return {
            "username": username,
            "ssn": user_data["ssn"],  # MAJOR PII VIOLATION
            "account_number": user_data["account_number"],
            "current_balance": user_data["balance"],
            "full_user_record": user_data  # SECURITY ISSUE 18: Over-sharing data
        }

# SECURITY ISSUE 19: Global authentication instance
auth_manager = UserAuthentication()

# BCRYPT ISSUE 9: Misusing bcrypt for non-password data
def generate_account_id(user_info: dict) -> str:
    """Generate account ID using bcrypt incorrectly"""
    
    # BCRYPT ISSUE 10: Using bcrypt for data that's not passwords
    user_string = f"{user_info['username']}{user_info['ssn']}"
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed_id = bcrypt.hashpw(user_string.encode(), salt)
    
    # SECURITY ISSUE 20: Exposing sensitive data in account ID generation
    return base64.b64encode(hashed_id).decode()[:16]

# SECURITY ISSUE 21: Password validation function with weak rules
def validate_password_strength(password: str) -> bool:
    """Validate password strength - INTENTIONALLY WEAK"""
    
    # SECURITY ISSUE 22: Extremely weak password requirements
    if len(password) >= 4:  # Way too short!
        return True
    
    return False

# BCRYPT ISSUE 11: Helper function with improper bcrypt usage
def create_reset_token(username: str, email: str) -> str:
    """Create password reset token using bcrypt incorrectly"""
    
    # BCRYPT ISSUE 12: Using bcrypt for temporary tokens
    reset_data = f"{username}:{email}:{datetime.now().isoformat()}"
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    
    # SECURITY ISSUE 23: Predictable reset token generation
    token = bcrypt.hashpw(reset_data.encode(), salt)
    
    return base64.b64encode(token).decode()
