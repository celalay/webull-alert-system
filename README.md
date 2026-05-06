# Stock Dip Alert System

A production-quality Python script that monitors a trusted stock watchlist and sends Gmail alerts when stocks are trading at significant discounts to their long-term moving averages.

## Purpose

This tool helps you identify buying opportunities by automatically scanning your watchlist for stocks trading below their technical averages. Alerts are triggered when the upside potential to return to the 200-day moving average is at least 8%.

## Features

- **Automated Monitoring**: Scan multiple stocks in a single run
- **Smart Alerts**: Multi-level classification based on upside potential
  - Watch (7-8% upside)
  - Good Opportunity (8-12% upside)
  - Deep Discount (12-20% upside)
  - Investigate Carefully (20%+ upside)
- **Comprehensive Analysis**: Tracks current price, MA200, 1-year average, and 3-month average
- **Email Notifications**: Professional HTML emails via Gmail
- **Security**: Uses environment variables and Gmail app passwords (no hardcoded secrets)
- **Production Ready**: Logging, error handling, and validation throughout

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Gmail account with an [app password](https://support.google.com/accounts/answer/185833) configured

### Setup

1. **Clone or download the repository**

   ```bash
   cd webull-alert-system
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   # Copy the example to create your .env file
   cp .env.example .env

   # Edit .env with your Gmail credentials
   # Required:
   # GMAIL_SENDER: Your Gmail address
   # GMAIL_APP_PASSWORD: Your 16-character Gmail app password
   # Optional:
   # GMAIL_RECIPIENT: Where to send alerts (defaults to GMAIL_SENDER)
   # LOG_LEVEL: INFO, DEBUG, WARNING, or ERROR (defaults to INFO)
   ```

5. **Create your watchlist**

   ```bash
   # Edit watchlist.txt with your stock tickers
   # One ticker per line, uppercase recommended
   # Lines starting with # are comments
   ```

## Usage

### Run the scanner

```bash
python src/main.py
```

### Run tests

```bash
python -m pytest tests/
# or
python -m unittest discover tests/
```

## Configuration

### watchlist.txt

One ticker symbol per line:

```
AAPL
MSFT
GOOGL
TSLA
# You can add comments
NVDA
```

### .env

Create from `.env.example` and populate the required values:

```
GMAIL_SENDER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
```

Optional values:

```bash
GMAIL_RECIPIENT=recipient@example.com
LOG_LEVEL=INFO
```

### Alert Thresholds

Modify `src/config.py` to adjust:

- `MIN_UPSIDE_FOR_ALERT`: Minimum upside percentage to trigger an alert (default: 8%)
- `MA200_PERIOD`: Trading days for 200-day MA (default: 200)
- `MA_1YEAR_PERIOD`: Trading days for 1-year average (default: 252)
- `MA_3MONTH_PERIOD`: Trading days for 3-month average (default: 63)

## Project Structure

```
webull-alert-system/
├── src/
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration and constants
│   ├── watchlist.py         # Watchlist loading and validation
│   ├── data_provider.py     # yfinance integration
│   ├── calculations.py      # Stock analysis logic
│   └── email_service.py     # Gmail integration
├── tests/
│   └── test_calculations.py # Unit tests for calculations
├── watchlist.txt            # Your stock watchlist
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── project_context.md       # Trading logic documentation
```

## Gmail Setup

This tool requires a Gmail app-specific password (not your regular password):

1. Enable 2-Step Verification on your Google Account
2. Go to https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer" (or your device type)
4. Google will generate a 16-character password
5. Copy this password into your `.env` file as `GMAIL_APP_PASSWORD`

**Security Note**: Never commit your `.env` file to version control. The `.gitignore` file is configured to exclude it.

## How It Works

1. **Load Watchlist**: Reads stock tickers from `watchlist.txt`
2. **Fetch Data**: Retrieves 1 year of historical price data via yfinance
3. **Calculate Metrics**:
   - Current price
   - 200-day moving average (MA200)
   - 1-year average price
   - 3-month average price
   - Upside percentages to each average
4. **Check Conditions**:
   - Is current price below MA200?
   - Is upside to MA200 >= 8%?
5. **Classify Alert**: Assigns level based on upside potential
6. **Send Email**: Dispatches alert with full analysis if conditions met

For detailed trading logic, see [project_context.md](project_context.md).

## Running on a Schedule

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily at specific time)
4. Set action to run: `python C:\path\to\webull-alert-system\src\main.py`

### macOS/Linux (Cron)

```bash
# Run daily at 4:00 PM
0 16 * * * cd /path/to/webull-alert-system && python src/main.py
```

## Testing

Run the unit test suite:

```bash
# Using unittest
python -m unittest discover tests/

# Using pytest (if installed)
pytest tests/
```

Current test coverage includes:
- Upside percentage calculations
- Alert level classification
- Alert triggering logic
- Stock analysis workflow

## Logging

Logs are printed to console with timestamps. Adjust `LOG_LEVEL` in `.env`:

- `DEBUG`: Verbose output for troubleshooting
- `INFO`: Normal operation (default)
- `WARNING`: Issues that don't stop execution
- `ERROR`: Problems requiring attention

## Troubleshooting

### "No data found for ticker"

- Verify the ticker symbol is correct
- Check your internet connection
- yfinance may have temporary issues; try again later

### "SMTP Authentication failed"

- Verify `GMAIL_SENDER` and `GMAIL_APP_PASSWORD` in `.env`
- Ensure 2-Step Verification is enabled on your Google Account
- Double-check the app password (should be 16 characters)

### "Email sent but not received"

- Check spam folder
- Verify `GMAIL_RECIPIENT` in `.env`
- Gmail may rate-limit; wait a few minutes and try again

### "Insufficient data for ticker"

- yfinance needs at least 200 trading days of history
- Stock may be too new; wait a few months and try again

## Security

- ✅ Environment variables for secrets (no hardcoding)
- ✅ `.gitignore` excludes `.env` file
- ✅ Uses Gmail app passwords (not your main password)
- ✅ No credential storage in logs
- ✅ Proper error handling without exposing sensitive info

## Performance

- Typically processes 10-20 stocks in 30-60 seconds
- Network-bound (depends on yfinance response times)
- Can be optimized with batch requests if needed

## License

MIT License - feel free to use and modify for your needs.

## Contributing

This is a personal tool, but you can fork and customize it for your own use.

## Support

For issues with:
- **yfinance**: See https://github.com/ranaroussi/yfinance
- **Gmail API**: See https://support.google.com/accounts/answer/185833
- **Python**: See https://www.python.org/

---

**Disclaimer**: This tool is for informational purposes only. Past performance does not guarantee future results. Always do your own due diligence before making investment decisions.
