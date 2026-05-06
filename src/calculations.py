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
    ma_alltime: float,
    ma200: float,
    ma_last_30_days: float,
    ma_last_quarter: float,
    week52_high: float,
    week52_low: float,
    week52_avg: float,
    min_upside_threshold: float = 8.0,
    min_drop_from_52week_threshold: float = 8.0,
) -> Dict:
    """
    Analyze a stock and return comprehensive metrics using dual-signal approach.
    
    Args:
        ticker: Stock ticker symbol
        current_price: Current stock price
        ma_alltime: All-time average price
        ma200: 200-day moving average
        ma_last_30_days: Last 30 calendar days average price
        ma_last_quarter: Last completed calendar quarter average price
        week52_high: 52-week high price
        week52_low: 52-week low price
        week52_avg: 52-week average price
        min_upside_threshold: Minimum upside for historical alert (default 8%)
        min_drop_from_52week_threshold: Minimum drop from 52-week avg for forecast alert (default 8%)
        
    Returns:
        Dictionary with analysis results including:
        - ticker: Stock ticker
        - current_price: Current price
        - ma_alltime, ma200, ma_last_30_days, ma_last_quarter: Historical metrics
        - week52_high, week52_low, week52_avg: 52-week metrics
        - upside_to_ma200: Upside to MA200 (historical signal)
        - drop_from_week52_avg: Drop from 52-week average (forecast signal)
        - alert_triggered: Boolean (True if EITHER signal meets threshold)
        - alert_level: Classification based on triggered signal
        - alert_source: "historical", "forecast", or "both"
    """
    # Historical signal
    upside_to_alltime = calculate_upside_percentage(current_price, ma_alltime)
    upside_to_ma200 = calculate_upside_percentage(current_price, ma200)
    upside_to_last_month = calculate_upside_percentage(current_price, ma_last_30_days)
    upside_to_last_quarter = calculate_upside_percentage(current_price, ma_last_quarter)
    
    # Forecast signal (drop from 52-week average)
    drop_from_week52_avg = calculate_upside_percentage(current_price, week52_avg)
    
    # Alert logic: trigger if EITHER condition is met
    historical_alert = should_alert(
        current_price, ma200, upside_to_ma200, min_upside_threshold
    )
    forecast_alert = drop_from_week52_avg <= -min_drop_from_52week_threshold
    
    alert_triggered = historical_alert or forecast_alert
    
    # Determine alert source and level
    if alert_triggered:
        if historical_alert and forecast_alert:
            alert_source = "both"
            # Use the stronger signal for level
            primary_signal = abs(drop_from_week52_avg) if abs(drop_from_week52_avg) > upside_to_ma200 else upside_to_ma200
        elif forecast_alert:
            alert_source = "forecast"
            primary_signal = abs(drop_from_week52_avg)
        else:
            alert_source = "historical"
            primary_signal = upside_to_ma200
        
        alert_level = classify_alert_level(primary_signal)
    else:
        alert_source = "none"
        alert_level = "no_alert"
    
    return {
        "ticker": ticker,
        "current_price": round(current_price, 2),
        "ma_alltime": round(ma_alltime, 2),
        "ma200": round(ma200, 2),
        "ma_last_30_days": round(ma_last_30_days, 2),
        "ma_last_quarter": round(ma_last_quarter, 2),
        "week52_high": round(week52_high, 2),
        "week52_low": round(week52_low, 2),
        "week52_avg": round(week52_avg, 2),
        "upside_to_alltime": round(upside_to_alltime, 2),
        "upside_to_ma200": round(upside_to_ma200, 2),
        "upside_to_last_30_days": round(upside_to_last_month, 2),
        "upside_to_last_quarter": round(upside_to_last_quarter, 2),
        "drop_from_week52_avg": round(drop_from_week52_avg, 2),
        "alert_triggered": alert_triggered,
        "alert_level": alert_level,
        "alert_source": alert_source,
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
