import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_provider import calculate_moving_averages

print("Calling calculate_moving_averages('BABA', 200)...")
print()

result = calculate_moving_averages(ticker="BABA", ma200_period=200)

if result:
    current_price, ma_alltime, ma200, ma_last_30_days, ma_last_quarter = result
    print(f"Current Price:      {current_price:.2f}")
    print(f"All-Time Average:   {ma_alltime:.2f}")
    print(f"MA200:              {ma200:.2f}")
    print(f"Last 30 Days:       {ma_last_30_days:.2f}")
    print(f"Last Quarter:       {ma_last_quarter:.2f}")
    print()
    print("Upside to MA200:", ((ma200 - current_price) / current_price) * 100, "%")
else:
    print("Function returned None!")
