"""Configuration and constants for the stock dip alert system."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Gmail configuration
# Required: sender email and Gmail app password.
# Optional: recipient defaults to sender when omitted.
GMAIL_SENDER = os.getenv("GMAIL_SENDER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GMAIL_RECIPIENT = os.getenv("GMAIL_RECIPIENT", GMAIL_SENDER)

# File paths
WATCHLIST_FILE = PROJECT_ROOT / "watchlist.txt"

# Alert thresholds and classifications
ALERT_THRESHOLDS = {
    "watch": 7.0,           # 7-8%
    "good": 8.0,            # 8-12%
    "deep_discount": 12.0,  # 12-20%
    "investigate": 20.0,    # 20%+
}

# Minimum upside required to send alert
MIN_UPSIDE_FOR_ALERT = 8.0

# Technical indicators periods (in days)
MA200_PERIOD = 200
MA_1YEAR_PERIOD = 252  # Trading days in a year
MA_3MONTH_PERIOD = 63   # Trading days in 3 months

# Logging is optional; INFO keeps normal console output.
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
