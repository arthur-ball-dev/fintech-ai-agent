"""
Main FastAPI Trading Platform Application
========================================
This file contains intentional architecture and security flaws for AI agent analysis.
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import sqlite3
import os
import logging

# ARCHITECTURE ISSUE 1: Global variables and tight coupling
DATABASE_CONNECTION = None
ACTIVE_ORDERS = {}
USER_SESSIONS = {}

# ARCHITECTURE ISSUE 2: FastAPI app with poor organization
app = FastAPI(title="Super Secure Trading Platform", version="1.0.0")

# SECURITY ISSUE 1: Basic auth without proper security
security = HTTPBasic()

# ARCHITECTURE ISSUE 3: Direct database connection in main file
def get_database():
    global DATABASE_CONNECTION
    if DATABASE_CONNECTION is None:
        # SECURITY ISSUE 2: Hardcoded database path, no encryption
        DATABASE_CONNECTION = sqlite3.connect("trading_data.db", check_same_thread=False)
    return DATABASE_CONNECTION

# ARCHITECTURE ISSUE 4: Business logic mixed with API routes
@app.post("/api/place_order")
async def place_order(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    """Place a trading order - MULTIPLE ISSUES HERE"""
    
    # SECURITY ISSUE 3: No input validation
    order_data = await request.json()
    
    # ARCHITECTURE ISSUE 5: Direct SQL in route handler
    db = get_database()
    cursor = db.cursor()
    
    # SECURITY ISSUE 4: SQL injection vulnerability
    query = f"INSERT INTO orders (user_id, symbol, quantity, price) VALUES ('{credentials.username}', '{order_data['symbol']}', {order_data['quantity']}, {order_data['price']})"
    cursor.execute(query)
    
    # RISK MANAGEMENT ISSUE 1: No position limits check
    # position_limit should be checked here but isn't!
    
    # ARCHITECTURE ISSUE 6: Blocking database operations
    db.commit()
    
    # SECURITY ISSUE 5: Sensitive data in logs
    logging.info(f"Order placed: {order_data} for user {credentials.username}")
    
    return {"status": "order_placed", "order_id": cursor.lastrowid}

# ARCHITECTURE ISSUE 7: Monolithic route with multiple responsibilities
@app.get("/api/user_portfolio/{user_id}")
async def get_portfolio(user_id: str):
    """Get user portfolio - SECURITY AND ARCHITECTURE ISSUES"""
    
    # SECURITY ISSUE 6: No authentication check
    # ARCHITECTURE ISSUE 8: Direct database access in route
    db = get_database()
    cursor = db.cursor()
    
    # SECURITY ISSUE 7: More SQL injection possibilities
    cursor.execute(f"SELECT * FROM portfolios WHERE user_id = '{user_id}'")
    portfolio = cursor.fetchall()
    
    # COMPLIANCE ISSUE 1: No audit trail for data access
    # ARCHITECTURE ISSUE 9: Raw database data returned without DTO
    return {"portfolio": portfolio}

# ARCHITECTURE ISSUE 10: Global error handler with sensitive info exposure
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler - SECURITY ISSUE"""
    
    # SECURITY ISSUE 8: Sensitive error information exposure
    return {
        "error": str(exc),
        "traceback": exc.__traceback__,
        "request_url": str(request.url),
        "request_headers": dict(request.headers)
    }

# ARCHITECTURE ISSUE 11: Startup logic in main file
@app.on_event("startup")
async def startup_event():
    """Application startup - POOR SEPARATION OF CONCERNS"""
    
    # ARCHITECTURE ISSUE 12: Database initialization mixed with app startup
    db = get_database()
    cursor = db.cursor()
    
    # SECURITY ISSUE 9: No SSL enforcement for database
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            symbol TEXT,
            quantity REAL,
            price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # COMPLIANCE ISSUE 2: No data retention policies
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolios (
            user_id TEXT,
            symbol TEXT,
            quantity REAL,
            avg_cost REAL
        )
    """)
    
    db.commit()

# ARCHITECTURE ISSUE 13: No proper configuration management
if __name__ == "__main__":
    import uvicorn
    
    # SECURITY ISSUE 10: Development server in production, no SSL
    uvicorn.run(
        app, 
        host="0.0.0.0",  # SECURITY ISSUE 11: Binding to all interfaces
        port=8000,
        debug=True,      # SECURITY ISSUE 12: Debug mode enabled
        reload=True      # ARCHITECTURE ISSUE 14: Auto-reload in production
    )
