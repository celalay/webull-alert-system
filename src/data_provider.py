"""Data provider for fetching historical price data using yfinance."""

from typing import Tuple, Optional
import logging

try:
    import yfinance as yf
except ImportError:
    raise ImportError(
        "yfinance is required. Install it with: pip install yfinance"
    )

logger = logging.getLogger(__name__)


def fetch_stock_data(
    ticker: str,
    period: str = "1y"
) -> Optional[object]:
    """
    Fetch stock data using yfinance.
    
    Args:
        ticker: Stock ticker symbol
        period: Period for historical data (default "1y" for 1 year)
        
    Returns:
        yfinance Ticker object or None if fetch fails
    """
    try:
        stock = yf.Ticker(ticker)
        # Try to fetch historical data to verify ticker is valid
        hist = stock.history(period=period)
        if hist.empty:
            logger.warning(f"No data found for ticker: {ticker}")
            return None
        return stock
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        return None


def get_current_price(ticker: str) -> Optional[float]:
    """
    Get the current price for a stock.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Current price as float, or None if unable to fetch
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Try multiple fields for current price (different sources have different fields)
        if "currentPrice" in info:
            return info["currentPrice"]
        elif "regularMarketPrice" in info:
            return info["regularMarketPrice"]
        elif "bid" in info and info["bid"] > 0:
            return info["bid"]
        
        logger.warning(f"Could not determine current price for {ticker}")
        return None
        
    except Exception as e:
        logger.error(f"Error fetching current price for {ticker}: {e}")
        return None


def calculate_moving_averages(
    ticker: str,
    ma200_period: int = 200,
    ma_1year_period: int = 252,
    ma_3month_period: int = 63
) -> Optional[Tuple[float, float, float, float]]:
    """
    Calculate moving averages for a stock.
    
    Args:
        ticker: Stock ticker symbol
        ma200_period: Number of trading days for MA200 (default 200)
        ma_1year_period: Number of trading days for 1-year average (default 252)
        ma_3month_period: Number of trading days for 3-month average (default 63)
        
    Returns:
        Tuple of (current_price, ma200, ma_1year, ma_3month)
        or None if unable to calculate
    """
    try:
        # Fetch 1 year of historical data to ensure we have enough for MA200
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        
        if hist.empty or len(hist) < ma200_period:
            logger.warning(
                f"Insufficient data for {ticker}. "
                f"Got {len(hist)} days, need at least {ma200_period}"
            )
            return None
        
        closing_prices = hist["Close"]
        
        # Get current price (most recent close)
        current_price = closing_prices.iloc[-1]
        
        # Calculate moving averages
        ma200 = closing_prices.tail(ma200_period).mean()
        ma_1year = closing_prices.tail(ma_1year_period).mean()
        ma_3month = closing_prices.tail(ma_3month_period).mean()
        
        return (float(current_price), float(ma200), float(ma_1year), float(ma_3month))
        
    except Exception as e:
        logger.error(f"Error calculating moving averages for {ticker}: {e}")
        return None


def get_stock_info(ticker: str) -> Optional[dict]:
    """
    Get general stock information.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Dictionary with stock info or None if unable to fetch
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "longName": info.get("longName", ticker),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "currency": info.get("currency", "USD"),
        }
        
    except Exception as e:
        logger.error(f"Error fetching stock info for {ticker}: {e}")
        return None
