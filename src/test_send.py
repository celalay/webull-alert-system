import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.email_service import send_email
from src.config import GMAIL_SENDER, GMAIL_APP_PASSWORD, GMAIL_RECIPIENT

if __name__ == "__main__":
    print(f"GMAIL_SENDER: {GMAIL_SENDER}")
    print(f"GMAIL_APP_PASSWORD length: {len(GMAIL_APP_PASSWORD) if GMAIL_APP_PASSWORD else 0}")
    print(f"GMAIL_RECIPIENT: {GMAIL_RECIPIENT}")
    
    ok = send_email(
        GMAIL_SENDER,
        GMAIL_APP_PASSWORD,
        GMAIL_RECIPIENT or GMAIL_SENDER,
        "Test Stock Dip Alert",
        "<p>This is a test email from your stock dip alert system.</p>",
    )
    print(f"Result: {ok}")
