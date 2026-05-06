"""Calculation logic for stock analysis and alert levels."""

from typing import Dict, Optional, Tuple


def calculate_upside_percentage(current_price: float, target_price: float) -> float:
    """
    Calculate upside percentage from current price to target price.
    
    Args:
        current_price: Current stock price
        target_price: Target/reference price (MA200, average, etc.)
        
    Returns:
        Upside percentage. Negative if current price is above target.
    """
    if current_price <= 0:
        return 0.0
    
    return ((target_price - current_price) / current_price) * 100


def classify_alert_level(upside_percentage: float) -> str:
    """
    Classify alert level based on upside percentage.
    
    Classification levels:
    - "watch": 7-8% upside
    - "good_opportunity": 8-12% upside
    - "deep_discount": 12-20% upside
    - "investigate_carefully": 20%+ upside
    
    Args:
        upside_percentage: Upside percentage to MA200
        
    Returns:
        Alert level classification string
    """
    if upside_percentage >= 20.0:
        return "investigate_carefully"
    elif upside_percentage >= 12.0:
        return "deep_discount"
    elif upside_percentage >= 8.0:
        return "good_opportunity"
    elif upside_percentage >= 7.0:
        return "watch"
    else:
        return "no_alert"


def should_alert(
    current_price: float,
    ma200: float,
    upside_to_ma200: float,
    min_upside_threshold: float = 8.0
) -> bool:
    """
    Determine if an alert should be triggered.
    
    Conditions:
    - Current price is below MA200
    - Upside to MA200 is >= min_upside_threshold
    
    Args:
        current_price: Current stock price
        ma200: 200-day moving average
        upside_to_ma200: Calculated upside to MA200 as percentage
        min_upside_threshold: Minimum upside percentage to trigger alert (default 8%)
        
    Returns:
        True if alert should be triggered, False otherwise
    """
    below_ma200 = current_price < ma200
    sufficient_upside = upside_to_ma200 >= min_upside_threshold
    
    return below_ma200 and sufficient_upside


def analyze_stock(
    ticker: str,
    current_price: float,
    ma200: float,
    ma_1year: float,
    ma_3month: float,
    min_upside_threshold: float = 8.0
) -> Dict:
    """
    Analyze a stock and return comprehensive metrics.
    
    Args:
        ticker: Stock ticker symbol
        current_price: Current stock price
        ma200: 200-day moving average
        ma_1year: 1-year average price
        ma_3month: 3-month average price
        min_upside_threshold: Minimum upside for alert
        
    Returns:
        Dictionary with analysis results including:
        - ticker: Stock ticker
        - current_price: Current price
        - ma200: 200-day MA
        - ma_1year: 1-year average
        - ma_3month: 3-month average
        - upside_to_ma200: Upside to MA200 as percentage
        - upside_to_1year: Upside to 1-year average as percentage
        - upside_to_3month: Upside to 3-month average as percentage
        - alert_triggered: Boolean for whether alert should be sent
        - alert_level: Classification of alert level
    """
    upside_to_ma200 = calculate_upside_percentage(current_price, ma200)
    upside_to_1year = calculate_upside_percentage(current_price, ma_1year)
    upside_to_3month = calculate_upside_percentage(current_price, ma_3month)
    
    alert_triggered = should_alert(
        current_price, ma200, upside_to_ma200, min_upside_threshold
    )
    alert_level = classify_alert_level(upside_to_ma200) if alert_triggered else "no_alert"
    
    return {
        "ticker": ticker,
        "current_price": round(current_price, 2),
        "ma200": round(ma200, 2),
        "ma_1year": round(ma_1year, 2),
        "ma_3month": round(ma_3month, 2),
        "upside_to_ma200": round(upside_to_ma200, 2),
        "upside_to_1year": round(upside_to_1year, 2),
        "upside_to_3month": round(upside_to_3month, 2),
        "alert_triggered": alert_triggered,
        "alert_level": alert_level,
    }


def format_alert_level_display(alert_level: str) -> str:
    """
    Format alert level for display in emails and logs.
    
    Args:
        alert_level: Internal alert level string
        
    Returns:
        Human-readable alert level string
    """
    level_display = {
        "watch": "⚠️ Watch (7-8% upside)",
        "good_opportunity": "✅ Good Opportunity (8-12% upside)",
        "deep_discount": "🔥 Deep Discount (12-20% upside)",
        "investigate_carefully": "🚨 Investigate Carefully (20%+ upside)",
        "no_alert": "No Alert",
    }
    
    return level_display.get(alert_level, alert_level)
