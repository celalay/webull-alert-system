"""Data provider for fetching historical price data using yfinance."""

from datetime import date, timedelta
from typing import Tuple, Optional
import logging

import pandas as pd

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


def _period_average(
    closing_prices: pd.Series,
    start_date: date,
    end_date: date,
) -> Optional[float]:
    """Calculate the average close price over an inclusive date range."""
    period_dates = closing_prices.index.date
    period_prices = closing_prices.loc[
        (period_dates >= start_date) & (period_dates <= end_date)
    ]

    if period_prices.empty:
        return None

    return float(period_prices.mean())


def _last_30_days_range(reference_date: date) -> tuple[date, date]:
    """Return the inclusive date range for the last 30 calendar days."""
    end_date = reference_date
    start_date = reference_date - timedelta(days=29)
    return start_date, end_date


def _previous_quarter_range(reference_date: date) -> tuple[date, date]:
    """Return the start and end date for the previous completed calendar quarter."""
    current_quarter_start_month = ((reference_date.month - 1) // 3) * 3 + 1
    current_quarter_start = date(reference_date.year, current_quarter_start_month, 1)
    previous_quarter_end = current_quarter_start - timedelta(days=1)
    previous_quarter_start_month = ((previous_quarter_end.month - 1) // 3) * 3 + 1
    previous_quarter_start = date(
        previous_quarter_end.year,
        previous_quarter_start_month,
        1,
    )
    return previous_quarter_start, previous_quarter_end


def calculate_moving_averages(
    ticker: str,
    ma200_period: int = 200,
) -> Optional[Tuple[float, float, float, float, float, float, float, float]]:
    """
    Calculate historical averages and 52-week forecast metrics for a stock.

    Args:
        ticker: Stock ticker symbol
        ma200_period: Number of trading days for MA200 (default 200)

    Returns:
        Tuple of (current_price, ma_alltime, ma200, ma_last_30_days, ma_last_quarter,
                  week52_high, week52_low, week52_avg)
        or None if unable to calculate
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="max")

        if hist.empty or len(hist) < ma200_period:
            logger.warning(
                f"Insufficient data for {ticker}. "
                f"Got {len(hist)} days, need at least {ma200_period}"
            )
            return None

        closing_prices = hist["Close"]
        current_price = float(closing_prices.iloc[-1])
        ma_alltime = float(closing_prices.mean())
        ma200 = float(closing_prices.tail(ma200_period).mean())

        reference_date = closing_prices.index[-1].date()
        last_month_start, last_month_end = _last_30_days_range(reference_date)
        last_quarter_start, last_quarter_end = _previous_quarter_range(reference_date)

        ma_last_month = _period_average(closing_prices, last_month_start, last_month_end)
        ma_last_quarter = _period_average(
            closing_prices,
            last_quarter_start,
            last_quarter_end,
        )

        if ma_last_month is None or ma_last_quarter is None:
            logger.warning(f"Insufficient calendar data for {ticker}")
            return None

        # Calculate 52-week metrics
        hist_52week = stock.history(period="1y")
        if not hist_52week.empty:
            week52_high = float(hist_52week["Close"].max())
            week52_low = float(hist_52week["Close"].min())
            week52_avg = float(hist_52week["Close"].mean())
        else:
            logger.warning(f"Insufficient 52-week data for {ticker}")
            return None

        logger.debug(
            f"[{ticker}] Raw values - Current: {current_price}, AllTime: {ma_alltime}, "
            f"MA200: {ma200}, Last30: {ma_last_month}, LastQtr: {ma_last_quarter}, "
            f"52wHigh: {week52_high}, 52wLow: {week52_low}, 52wAvg: {week52_avg}"
        )

        return (
            current_price,
            ma_alltime,
            ma200,
            ma_last_month,
            ma_last_quarter,
            week52_high,
            week52_low,
            week52_avg,
        )

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
