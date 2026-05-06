"""Main entry point for stock dip alert system."""

import sys
import logging
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    WATCHLIST_FILE,
    GMAIL_SENDER,
    GMAIL_APP_PASSWORD,
    GMAIL_RECIPIENT,
    MIN_UPSIDE_FOR_ALERT,
    MA200_PERIOD,
    LOG_LEVEL,
)
from watchlist import load_watchlist, validate_tickers
from data_provider import calculate_moving_averages, get_stock_info
from calculations import analyze_stock
from email_service import send_summary_email

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def validate_configuration() -> bool:
    """
    Validate that all required configuration is present.
    
    Returns:
        True if configuration is valid, False otherwise
    """
    errors = []

    # Only the sender and app password are required.
    # Recipient defaults to the sender, and logging defaults to INFO.
    
    if not GMAIL_SENDER:
        errors.append("GMAIL_SENDER not set in .env file")
    
    if not GMAIL_APP_PASSWORD:
        errors.append("GMAIL_APP_PASSWORD not set in .env file")
    
    if not WATCHLIST_FILE.exists():
        errors.append(f"Watchlist file not found: {WATCHLIST_FILE}")
    
    if errors:
        logger.error("Configuration errors:")
        for error in errors:
            logger.error(f"  - {error}")
        return False
    
    return True


def run_scan() -> None:
    """Run the stock dip scan and send alerts."""
    logger.info("Starting stock dip alert scan...")
    
    # Validate configuration
    if not validate_configuration():
        logger.error("Configuration validation failed. Exiting.")
        sys.exit(1)
    
    # Load watchlist
    try:
        tickers = load_watchlist(WATCHLIST_FILE)
        tickers = validate_tickers(tickers)
        logger.info(f"Loaded {len(tickers)} tickers from watchlist")
    except FileNotFoundError as e:
        logger.error(f"Error loading watchlist: {e}")
        sys.exit(1)
    
    if not tickers:
        logger.warning("No valid tickers found in watchlist")
        return
    
    # Analyze each stock
    alerts = []
    errors_count = 0
    
    for ticker in tickers:
        logger.info(f"Analyzing {ticker}...")
        
        try:
            # Get moving averages and current price
            data = calculate_moving_averages(ticker=ticker, ma200_period=MA200_PERIOD)
            
            if data is None:
                logger.warning(f"Could not fetch data for {ticker}. Skipping.")
                errors_count += 1
                continue
            
            current_price, ma_alltime, ma200, ma_last_30_days, ma_last_quarter = data
            
            # Analyze stock
            analysis = analyze_stock(
                ticker=ticker,
                current_price=current_price,
                ma_alltime=ma_alltime,
                ma200=ma200,
                ma_last_30_days=ma_last_30_days,
                ma_last_quarter=ma_last_quarter,
                min_upside_threshold=MIN_UPSIDE_FOR_ALERT,
            )
            
            # Log analysis results
            logger.info(
                f"{ticker}: Price=${analysis['current_price']}, "
                f"All-Time=${analysis['ma_alltime']}, "
                f"MA200=${analysis['ma200']}, "
                f"Last 30 Days=${analysis['ma_last_30_days']}, "
                f"Last Quarter=${analysis['ma_last_quarter']}, "
                f"Upside={analysis['upside_to_ma200']}%"
            )
            
            # Collect alert if triggered
            if analysis["alert_triggered"]:
                logger.info(
                    f"Alert triggered for {ticker}! "
                    f"Level: {analysis['alert_level']}"
                )
                
                # Get company info
                stock_info = get_stock_info(ticker)
                company_name = stock_info.get("longName") if stock_info else None
                
                # Add to alerts list
                alerts.append({
                    "ticker": ticker,
                    "company_name": company_name,
                    "current_price": analysis["current_price"],
                    "ma_alltime": analysis["ma_alltime"],
                    "ma200": analysis["ma200"],
                    "ma_last_30_days": analysis["ma_last_30_days"],
                    "ma_last_quarter": analysis["ma_last_quarter"],
                    "upside_to_alltime": analysis["upside_to_alltime"],
                    "upside_to_ma200": analysis["upside_to_ma200"],
                    "upside_to_last_30_days": analysis["upside_to_last_30_days"],
                    "upside_to_last_quarter": analysis["upside_to_last_quarter"],
                    "alert_level": analysis["alert_level"],
                })
        
        except Exception as e:
            logger.error(f"Error processing {ticker}: {e}", exc_info=True)
            errors_count += 1
    
    # Send summary email with all alerts
    if alerts:
        email_sent = send_summary_email(
            sender=GMAIL_SENDER,
            app_password=GMAIL_APP_PASSWORD,
            recipient=GMAIL_RECIPIENT,
            alerts=alerts,
        )
        if not email_sent:
            logger.error("Failed to send summary email")
            errors_count += 1
    
    # Summary
    logger.info(f"Scan complete. Alerts sent: {len(alerts)}, Errors: {errors_count}")


if __name__ == "__main__":
    run_scan()
