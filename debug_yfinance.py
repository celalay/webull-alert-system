import yfinance as yf

print("=" * 60)
print("Test 1: Fresh call - period='max'")
print("=" * 60)

stock1 = yf.Ticker("BABA")
hist1 = stock1.history(period="max")

print(f"Data points: {len(hist1)}")
print(f"Date range: {hist1.index[0].date()} to {hist1.index[-1].date()}")
print(f"Current Price: {hist1['Close'].iloc[-1]:.2f}")
print(f"All-Time Average: {hist1['Close'].mean():.2f}")
print(f"MA200 (last 200): {hist1['Close'].tail(200).mean():.2f}")

print("\n" + "=" * 60)
print("Test 2: Fresh call - period='max' (again)")
print("=" * 60)

stock2 = yf.Ticker("BABA")
hist2 = stock2.history(period="max")

print(f"Data points: {len(hist2)}")
print(f"Date range: {hist2.index[0].date()} to {hist2.index[-1].date()}")
print(f"Current Price: {hist2['Close'].iloc[-1]:.2f}")
print(f"All-Time Average: {hist2['Close'].mean():.2f}")
print(f"MA200 (last 200): {hist2['Close'].tail(200).mean():.2f}")

print("\n" + "=" * 60)
print("Comparison:")
print("=" * 60)
print(f"Same data? {hist1['Close'].equals(hist2['Close'])}")
print(f"Same length? {len(hist1) == len(hist2)}")
