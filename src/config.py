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

# Minimum upside required to send alert (historical metric)
MIN_UPSIDE_FOR_ALERT = 8.0

# Minimum drop from 52-week average to trigger forecast alert
MIN_DROP_FROM_52WEEK_AVG = 8.0

# Technical indicator period (in days)
MA200_PERIOD = 200

# Logging is optional; INFO keeps normal console output.
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
