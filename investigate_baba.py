import yfinance as yf
import pandas as pd
from datetime import datetime

print("=" * 80)
print("INVESTIGATING BABA DATA DISCREPANCY")
print("=" * 80)

ticker = "BABA"
stock = yf.Ticker(ticker)

# Get different periods
print("\n1. Checking different yfinance periods:")
print("-" * 80)

for period in ["1y", "2y", "5y", "10y", "max"]:
    hist = stock.history(period=period)
    if not hist.empty:
        print(f"\nPeriod: {period}")
        print(f"  Data points: {len(hist)}")
        print(f"  Date range: {hist.index[0].date()} to {hist.index[-1].date()}")
        print(f"  Current (last close): {hist['Close'].iloc[-1]:.2f}")
        print(f"  All-time avg: {hist['Close'].mean():.2f}")
        print(f"  MA200: {hist['Close'].tail(200).mean():.2f}")

# Get full data and inspect
print("\n\n2. Checking FULL historical data (period='max'):")
print("-" * 80)

hist_full = stock.history(period="max")
print(f"Total rows: {len(hist_full)}")
print(f"\nFirst 5 rows:")
print(hist_full.head())
print(f"\nLast 5 rows:")
print(hist_full.tail())

# Check for any NaN or unusual values
print(f"\n\n3. Data quality checks:")
print("-" * 80)
print(f"Null values in Close: {hist_full['Close'].isnull().sum()}")
print(f"Min Close: {hist_full['Close'].min():.2f} on {hist_full['Close'].idxmin().date()}")
print(f"Max Close: {hist_full['Close'].max():.2f} on {hist_full['Close'].idxmax().date()}")
print(f"Mean: {hist_full['Close'].mean():.2f}")
print(f"Median: {hist_full['Close'].median():.2f}")

# Check recent 200 days
print(f"\n\n4. MA200 analysis (last 200 trading days):")
print("-" * 80)
last_200 = hist_full['Close'].tail(200)
print(f"Count: {len(last_200)}")
print(f"Mean: {last_200.mean():.2f}")
print(f"Min: {last_200.min():.2f}")
print(f"Max: {last_200.max():.2f}")
print(f"First date: {last_200.index[0].date()}")
print(f"Last date: {last_200.index[-1].date()}")
