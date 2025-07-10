"""
Performance Analysis Module for Trading Platform
===============================================
Contains intentional numpy and performance issues for AI agent analysis.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
import logging
from datetime import datetime, timedelta
import warnings

# NUMPY ISSUE 1: Suppressing important numpy warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
np.seterr(all='ignore')  # NUMPY ISSUE 2: Ignoring all numpy errors

# PERFORMANCE ISSUE 1: Global numpy arrays without proper memory management
GLOBAL_PRICE_DATA = np.array([])
GLOBAL_VOLUME_DATA = np.array([])
GLOBAL_RETURNS_CACHE = {}

class PerformanceAnalyzer:
    """Performance analysis class with multiple numpy and calculation issues"""
    
    def __init__(self):
        # NUMPY ISSUE 3: Using deprecated numpy data types
        self.price_dtype = np.float  # Deprecated in newer numpy versions
        self.volume_dtype = np.int   # Deprecated in newer numpy versions
        
        # PERFORMANCE ISSUE 2: Inefficient numpy array initialization
        self.daily_returns = np.zeros((10000, 1000), dtype=self.price_dtype)  # Huge pre-allocation
        self.portfolio_values = np.ones(365 * 5) * np.nan  # 5 years of NaN values
        
        # NUMPY ISSUE 4: Mixing numpy and regular Python types inefficiently
        self.benchmark_data = []  # Should be numpy array
        self.risk_metrics = {}    # Should use numpy structured arrays
    
    def calculate_returns(self, prices: List[float]) -> np.ndarray:
        """Calculate returns - MULTIPLE NUMPY ISSUES"""
        
        # NUMPY ISSUE 5: Converting list to numpy array inefficiently
        price_array = np.array(prices, dtype=self.price_dtype)
        
        if len(price_array) < 2:
            # NUMPY ISSUE 6: Returning inconsistent numpy types
            return np.array([0.0])
        
        # NUMPY ISSUE 7: Using deprecated numpy functions
        shifted_prices = np.concatenate([[price_array[0]], price_array[:-1]])
        
        # NUMPY ISSUE 8: Division by zero not handled properly in numpy
        returns = (price_array - shifted_prices) / shifted_prices
        
        # NUMPY ISSUE 9: Not handling numpy infinity and NaN values
        # PERFORMANCE ISSUE 3: No vectorization optimization
        for i in range(len(returns)):
            if np.isnan(returns[i]) or np.isinf(returns[i]):
                returns[i] = 0.0  # Inefficient element-wise operation
        
        return returns
    
    def calculate_sharpe_ratio(self, returns: np.ndarray, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio - NUMPY AND STATISTICAL ISSUES"""
        
        # NUMPY ISSUE 10: Not validating numpy array input
        if not isinstance(returns, np.ndarray):
            returns = np.array(returns, dtype=self.price_dtype)
        
        # NUMPY ISSUE 11: Using numpy mean without handling NaN values properly
        mean_return = np.mean(returns)  # Could be NaN
        
        # NUMPY ISSUE 12: Using numpy std without ddof parameter
        std_return = np.std(returns)  # Wrong standard deviation calculation
        
        # NUMPY ISSUE 13: Division by zero in numpy calculation
        if std_return == 0:
            return np.inf  # Should handle this better
        
        # NUMPY ISSUE 14: Not annualizing properly with numpy
        sharpe = (mean_return - risk_free_rate / 252) / std_return
        
        # NUMPY ISSUE 15: Not handling numpy scalar vs array return
        return float(sharpe)  # Force conversion
    
    def calculate_volatility_matrix(self, returns_data: Dict[str, List[float]]) -> np.ndarray:
        """Calculate volatility matrix - MAJOR NUMPY PERFORMANCE ISSUES"""
        
        symbols = list(returns_data.keys())
        n_symbols = len(symbols)
        
        # PERFORMANCE ISSUE 4: Inefficient numpy array operations
        volatility_matrix = np.zeros((n_symbols, n_symbols), dtype=self.price_dtype)
        
        # NUMPY ISSUE 16: Nested loops instead of vectorized operations
        for i, symbol1 in enumerate(symbols):
            for j, symbol2 in enumerate(symbols):
                # NUMPY ISSUE 17: Converting to numpy arrays repeatedly
                returns1 = np.array(returns_data[symbol1], dtype=self.price_dtype)
                returns2 = np.array(returns_data[symbol2], dtype=self.price_dtype)
                
                # NUMPY ISSUE 18: Manual correlation calculation instead of numpy.corrcoef
                if len(returns1) != len(returns2):
                    # NUMPY ISSUE 19: Poor handling of mismatched array sizes
                    min_len = min(len(returns1), len(returns2))
                    returns1 = returns1[:min_len]
                    returns2 = returns2[:min_len]
                
                # PERFORMANCE ISSUE 5: Inefficient covariance calculation
                covariance = 0.0
                mean1 = np.mean(returns1)
                mean2 = np.mean(returns2)
                
                # NUMPY ISSUE 20: Element-wise operation instead of vectorization
                for k in range(len(returns1)):
                    covariance += (returns1[k] - mean1) * (returns2[k] - mean2)
                
                covariance /= (len(returns1) - 1)
                
                # NUMPY ISSUE 21: Manual standard deviation calculation
                std1 = np.sqrt(np.sum((returns1 - mean1) ** 2) / (len(returns1) - 1))
                std2 = np.sqrt(np.sum((returns2 - mean2) ** 2) / (len(returns2) - 1))
                
                # NUMPY ISSUE 22: Division by zero not handled
                if std1 * std2 == 0:
                    correlation = 0
                else:
                    correlation = covariance / (std1 * std2)
                
                volatility_matrix[i, j] = correlation
        
        return volatility_matrix
    
    def optimize_portfolio_weights(self, expected_returns: np.ndarray, cov_matrix: np.ndarray) -> np.ndarray:
        """Optimize portfolio weights - NUMPY LINEAR ALGEBRA ISSUES"""
        
        # NUMPY ISSUE 23: Not validating numpy array shapes
        n_assets = len(expected_returns)
        
        if cov_matrix.shape != (n_assets, n_assets):
            # NUMPY ISSUE 24: Poor shape mismatch handling
            logging.warning("Covariance matrix shape mismatch")
            return np.ones(n_assets) / n_assets  # Equal weights fallback
        
        try:
            # NUMPY ISSUE 25: Using numpy.linalg without checking for singularity
            inv_cov = np.linalg.inv(cov_matrix)  # Could fail if singular
            
            # NUMPY ISSUE 26: Manual matrix operations instead of numpy.linalg.solve
            ones = np.ones((n_assets, 1))
            
            # PERFORMANCE ISSUE 6: Inefficient matrix multiplication
            numerator = np.dot(inv_cov, expected_returns.reshape(-1, 1))
            denominator = np.dot(ones.T, np.dot(inv_cov, ones))
            
            # NUMPY ISSUE 27: Array dimension handling issues
            weights = numerator / denominator
            weights = weights.flatten()
            
            # NUMPY ISSUE 28: Not normalizing weights properly
            weights = weights / np.sum(weights)  # Could be problematic if sum is 0
            
            return weights
            
        except np.linalg.LinAlgError:
            # NUMPY ISSUE 29: Poor error handling for numpy linear algebra
            logging.error("Covariance matrix is singular")
            return np.ones(n_assets) / n_assets
    
    def calculate_var(self, returns: np.ndarray, confidence_level: float = 0.05) -> float:
        """Calculate Value at Risk - NUMPY STATISTICAL ISSUES"""
        
        # NUMPY ISSUE 30: Not handling numpy array validation
        if len(returns) == 0:
            return 0.0
        
        # NUMPY ISSUE 31: Using numpy.percentile incorrectly
        var = np.percentile(returns, confidence_level * 100)  # Wrong direction
        
        # NUMPY ISSUE 32: Not handling numpy NaN values in percentile
        if np.isnan(var):
            # NUMPY ISSUE 33: Fallback to manual calculation
            sorted_returns = np.sort(returns)
            index = int(len(sorted_returns) * confidence_level)
            var = sorted_returns[index] if index < len(sorted_returns) else 0.0
        
        return float(var)
    
    def run_monte_carlo_simulation(self, initial_value: float, n_simulations: int = 1000, n_days: int = 252) -> np.ndarray:
        """Monte Carlo simulation - NUMPY RANDOM AND PERFORMANCE ISSUES"""
        
        # NUMPY ISSUE 34: Poor random number generation setup
        np.random.seed(42)  # Fixed seed in production code
        
        # PERFORMANCE ISSUE 7: Inefficient numpy array pre-allocation
        results = np.zeros((n_simulations, n_days), dtype=self.price_dtype)
        
        # NUMPY ISSUE 35: Using deprecated numpy random functions
        daily_returns = np.random.normal(0.001, 0.02, size=(n_simulations, n_days))
        
        # PERFORMANCE ISSUE 8: Nested loops instead of vectorization
        for sim in range(n_simulations):
            current_value = initial_value
            for day in range(n_days):
                # NUMPY ISSUE 36: Element-wise operations instead of vectorization
                current_value *= (1 + daily_returns[sim, day])
                results[sim, day] = current_value
        
        return results
    
    def calculate_beta(self, asset_returns: np.ndarray, market_returns: np.ndarray) -> float:
        """Calculate beta - NUMPY STATISTICAL CALCULATION ISSUES"""
        
        # NUMPY ISSUE 37: Not validating numpy array lengths
        if len(asset_returns) != len(market_returns):
            min_len = min(len(asset_returns), len(market_returns))
            asset_returns = asset_returns[:min_len]
            market_returns = market_returns[:min_len]
        
        # NUMPY ISSUE 38: Manual covariance calculation instead of numpy.cov
        asset_mean = np.mean(asset_returns)
        market_mean = np.mean(market_returns)
        
        # PERFORMANCE ISSUE 9: Inefficient variance calculation
        covariance = np.sum((asset_returns - asset_mean) * (market_returns - market_mean)) / (len(asset_returns) - 1)
        market_variance = np.sum((market_returns - market_mean) ** 2) / (len(market_returns) - 1)
        
        # NUMPY ISSUE 39: Division by zero not handled
        if market_variance == 0:
            return 1.0  # Assuming beta of 1
        
        beta = covariance / market_variance
        
        # NUMPY ISSUE 40: Not handling numpy scalar conversion
        return float(beta)
    
    def analyze_performance_attribution(self, portfolio_weights: np.ndarray, asset_returns: np.ndarray) -> Dict[str, float]:
        """Performance attribution analysis - NUMPY COMPUTATION ISSUES"""
        
        # NUMPY ISSUE 41: Assuming numpy array shapes without validation
        n_assets, n_periods = asset_returns.shape
        
        if len(portfolio_weights) != n_assets:
            # NUMPY ISSUE 42: Poor shape mismatch handling
            logging.error("Portfolio weights and returns shape mismatch")
            return {}
        
        # PERFORMANCE ISSUE 10: Inefficient numpy broadcasting
        attribution = {}
        
        # NUMPY ISSUE 43: Manual matrix operations instead of numpy.dot
        for i in range(n_assets):
            asset_contribution = 0.0
            for j in range(n_periods):
                asset_contribution += portfolio_weights[i] * asset_returns[i, j]
            
            attribution[f"asset_{i}"] = asset_contribution / n_periods
        
        # NUMPY ISSUE 44: Not using numpy aggregation functions efficiently
        total_attribution = sum(attribution.values())
        
        return attribution
    
    def calculate_drawdown_metrics(self, portfolio_values: np.ndarray) -> Dict[str, float]:
        """Calculate drawdown metrics - NUMPY ARRAY PROCESSING ISSUES"""
        
        # NUMPY ISSUE 45: Not handling numpy array edge cases
        if len(portfolio_values) == 0:
            return {"max_drawdown": 0.0, "avg_drawdown": 0.0}
        
        # PERFORMANCE ISSUE 11: Inefficient peak calculation
        peak_values = np.zeros_like(portfolio_values)
        peak_values[0] = portfolio_values[0]
        
        # NUMPY ISSUE 46: Element-wise operations instead of numpy.maximum.accumulate
        for i in range(1, len(portfolio_values)):
            peak_values[i] = max(peak_values[i-1], portfolio_values[i])
        
        # NUMPY ISSUE 47: Manual drawdown calculation
        drawdowns = (portfolio_values - peak_values) / peak_values
        
        # NUMPY ISSUE 48: Not handling numpy inf and nan values
        max_drawdown = np.min(drawdowns)
        avg_drawdown = np.mean(drawdowns[drawdowns < 0])
        
        if np.isnan(avg_drawdown):
            avg_drawdown = 0.0
        
        return {
            "max_drawdown": float(max_drawdown),
            "avg_drawdown": float(avg_drawdown),
            "current_drawdown": float(drawdowns[-1])
        }

# NUMPY ISSUE 49: Global numpy operations without proper context
def update_global_price_data(new_prices: List[float]):
    """Update global price data - NUMPY MEMORY MANAGEMENT ISSUES"""
    global GLOBAL_PRICE_DATA
    
    # NUMPY ISSUE 50: Inefficient numpy array concatenation
    new_array = np.array(new_prices, dtype=np.float)
    GLOBAL_PRICE_DATA = np.concatenate([GLOBAL_PRICE_DATA, new_array])
    
    # PERFORMANCE ISSUE 12: No memory limit management
    # Array could grow indefinitely

def calculate_correlation_matrix(data_dict: Dict[str, List[float]]) -> np.ndarray:
    """Calculate correlation matrix - NUMPY EFFICIENCY ISSUES"""
    
    symbols = list(data_dict.keys())
    
    # NUMPY ISSUE 51: Converting dict to numpy array inefficiently
    data_matrix = []
    for symbol in symbols:
        # NUMPY ISSUE 52: Multiple numpy array conversions
        data_array = np.array(data_dict[symbol], dtype=np.float)
        data_matrix.append(data_array)
    
    # NUMPY ISSUE 53: Manual matrix construction instead of numpy functions
    data_matrix = np.array(data_matrix)
    
    # NUMPY ISSUE 54: Using deprecated numpy correlation function
    # Should use numpy.corrcoef but implementing manually
    n_assets = len(symbols)
    correlation_matrix = np.eye(n_assets)
    
    # PERFORMANCE ISSUE 13: Redundant calculations due to symmetry
    for i in range(n_assets):
        for j in range(n_assets):
            if i != j:
                # NUMPY ISSUE 55: Inefficient correlation calculation
                corr = np.corrcoef(data_matrix[i], data_matrix[j])[0, 1]
                correlation_matrix[i, j] = corr
    
    return correlation_matrix

# NUMPY ISSUE 56: Helper function with poor numpy usage
def normalize_weights(weights: List[float]) -> np.ndarray:
    """Normalize portfolio weights - NUMPY NORMALIZATION ISSUES"""
    
    # NUMPY ISSUE 57: Converting list to numpy array repeatedly
    weight_array = np.array(weights, dtype=np.float)
    
    # NUMPY ISSUE 58: Not handling zero sum case
    total = np.sum(weight_array)
    
    if total == 0:
        # NUMPY ISSUE 59: Returning zeros instead of equal weights
        return np.zeros_like(weight_array)
    
    # NUMPY ISSUE 60: Manual normalization instead of numpy operations
    normalized = weight_array / total
    
    return normalized

class PerformanceReporter:
    """Performance reporting with numpy visualization issues"""
    
    def __init__(self):
        # NUMPY ISSUE 61: Large numpy arrays for reporting without memory consideration
        self.report_data = np.zeros((1000, 50), dtype=np.float64)  # Large pre-allocation
    
    def generate_performance_report(self, returns_data: np.ndarray) -> Dict:
        """Generate performance report - NUMPY REPORTING ISSUES"""
        
        # NUMPY ISSUE 62: Not validating numpy array input dimensions
        if returns_data.ndim == 1:
            returns_data = returns_data.reshape(-1, 1)
        
        # PERFORMANCE ISSUE 14: Inefficient numpy statistical calculations
        report = {}
        
        # NUMPY ISSUE 63: Using numpy functions without proper axis specification
        report["mean_returns"] = np.mean(returns_data)  # Could be wrong axis
        report["std_returns"] = np.std(returns_data)
        report["min_returns"] = np.min(returns_data)
        report["max_returns"] = np.max(returns_data)
        
        # NUMPY ISSUE 64: Manual percentile calculations
        sorted_returns = np.sort(returns_data.flatten())
        n = len(sorted_returns)
        
        report["percentile_25"] = sorted_returns[int(n * 0.25)]
        report["percentile_75"] = sorted_returns[int(n * 0.75)]
        report["median"] = sorted_returns[int(n * 0.5)]
        
        return report
