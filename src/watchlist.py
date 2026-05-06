"""Watchlist management for stock dip alerts."""

from pathlib import Path
from typing import List


def load_watchlist(watchlist_file: Path) -> List[str]:
    """
    Load tickers from watchlist file.
    
    Each line in the file should contain one ticker symbol.
    Lines starting with '#' are treated as comments.
    Empty lines are ignored.
    
    Args:
        watchlist_file: Path to the watchlist.txt file
        
    Returns:
        List of ticker symbols (uppercase)
        
    Raises:
        FileNotFoundError: If watchlist file doesn't exist
    """
    if not watchlist_file.exists():
        raise FileNotFoundError(f"Watchlist file not found: {watchlist_file}")
    
    tickers = []
    with open(watchlist_file, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Convert to uppercase and add
            ticker = line.upper()
            tickers.append(ticker)
    
    return tickers


def validate_tickers(tickers: List[str]) -> List[str]:
    """
    Validate and clean ticker symbols.
    
    Args:
        tickers: List of ticker symbols
        
    Returns:
        List of validated ticker symbols
    """
    validated = []
    for ticker in tickers:
        # Remove whitespace and convert to uppercase
        cleaned = ticker.strip().upper()
        # Basic validation: ticker should be 1-5 characters, alphanumeric
        if 1 <= len(cleaned) <= 5 and cleaned.isalnum():
            validated.append(cleaned)
    
    return validated
