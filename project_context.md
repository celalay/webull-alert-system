# Stock Dip Alert System - Project Context & Trading Logic

## Purpose

The Stock Dip Alert System identifies buying opportunities by monitoring when quality stocks temporarily trade below their historical average prices. The system specifically looks for situations where the upside to return to the stock's 200-day moving average is at least 8%.

## Core Trading Principles

### Why Monitor Below MA200?

The 200-day moving average (MA200) is a widely-used indicator of long-term trend:
- **Above MA200**: Stock is in an uptrend
- **Below MA200**: Stock is in a downtrend or correction
- **Far below MA200**: Potential dip buying opportunity

Stocks trading significantly below their MA200 often represent temporary dislocations rather than fundamental deterioration, especially for quality companies on your watchlist.

### The 8% Upside Threshold

The minimum 8% upside requirement ensures:
- **Statistical Significance**: Not chasing trivial 1-2% gains
- **Risk/Reward**: Worth the execution and monitoring effort
- **No Upper Cap**: If a stock offers 12%, 20%, or 50% upside, it's still flagged

This is intentionally mechanical to avoid emotional decision-making.

## Calculation Methodology

### Key Metrics

For each stock, the system calculates:

1. **Current Price**: Latest closing price from yfinance
2. **200-Day Moving Average (MA200)**: Average of the last 200 trading days
3. **1-Year Average**: Average price over the past 252 trading days (1 year of markets)
4. **3-Month Average**: Average price over the past 63 trading days (3 months of markets)

### Upside Calculations

All upside percentages use this formula:

```
Upside % = ((Target Price - Current Price) / Current Price) * 100
```

Where:
- **Current Price** = Today's closing price
- **Target Price** = MA200, 1-year average, or 3-month average
- **Positive result** = Upside potential
- **Negative result** = Current price is above the target (downside)

### Example

If a stock is trading at $100 and its MA200 is $108:
- Upside = ((108 - 100) / 100) * 100 = 8%
- This meets the minimum threshold → Alert triggered

## Alert Conditions

An alert is triggered when **BOTH** conditions are true:

1. ✅ Current price is **below** MA200
2. ✅ Upside to MA200 is **>= 8%**

### What Triggers Each Alert Level

- **Watch (7-8%)**: Slight dip, monitor for potential entry
- **Good Opportunity (8-12%)**: Meaningful dip with reasonable upside
- **Deep Discount (12-20%)**: Significant dip, worth investigating
- **Investigate Carefully (20%+)**: Major dip, requires thorough analysis

The "+ carefully" language on the 20%+ tier reflects reality: a 20% gap to MA200 suggests either:
- Temporary overreaction in market (buying opportunity)
- Potential emerging problem (needs research)

The system flags it; you decide which case applies.

## What You Get in Each Alert

### Email Content

Each alert email includes:

- **Ticker & Company Name**: Quick identification
- **Alert Level**: Visual emoji and classification
- **Current Price**: What the stock is trading at now
- **MA200 Value**: The 200-day average for reference
- **Upside to MA200**: The key metric (8%, 12%, etc.)
- **1-Year Average**: For historical context
- **3-Month Average**: For shorter-term context
- **All Upside %s**: To each reference point
- **Summary**: Clear explanation of the opportunity

### Example Alert

```
Current Price: $95
MA200: $110
1-Year Average: $105
3-Month Average: $98

Upside to MA200: 15.79% ← KEY METRIC
Alert Level: Deep Discount (12-20% upside)
```

This means: "If the stock returns to its 200-day average, it could provide 15.79% upside."

## Technical Implementation

### Data Sources

- **yfinance**: Reliable, free source for historical OHLCV data
- **Historical Period**: 1+ year of data for accurate MA200 and averages
- **Frequency**: Close prices only (simpler than intraday)

### Calculation Periods

- **MA200**: Last 200 trading days (≈ 10 months)
- **1-Year Average**: Last 252 trading days (≈ 12 months, standard market calendar)
- **3-Month Average**: Last 63 trading days (≈ 3 months, standard market calendar)

These are industry-standard periods; they can be customized in `config.py`.

### Email Delivery

- **Service**: Gmail SMTP (reliable, widely-supported)
- **Authentication**: App-specific passwords (secure, doesn't expose main password)
- **Format**: HTML for professional presentation
- **Timing**: Sent immediately when condition is met

## No Upsell Ceilings

Intentionally, there is **no upper limit** on upside alerts. If a stock offers:
- 8% upside → Alert
- 15% upside → Alert
- 35% upside → Alert
- 150% upside → Alert

The system flags all of them. This prevents missing exceptional opportunities while still filtering noise.

## Edge Cases & Validation

### What's NOT Flagged

- **Stock above MA200**: Not in "dip" territory
- **Stock below MA200 but <8% upside**: Insufficient potential
- **Stock with <200 days of history**: Data too limited
- **Invalid tickers**: Skipped with logging

### Watchlist Validation

- Tickers are normalized to uppercase
- Comments (lines starting with `#`) are ignored
- Empty lines are skipped
- 1-5 character alphanumeric strings only

## Security & Privacy

- **No secrets in code**: All configuration via `.env`
- **No logging of sensitive data**: Credentials never written to logs
- **Git safety**: `.gitignore` excludes `.env` and sensitive files
- **Email headers**: Sender/recipient properly configured, no data leaks

## Workflow for Manual Operation

**Typical usage pattern:**

1. Run `python src/main.py` manually or on schedule
2. System scans watchlist against latest market data
3. Alerts arrive only for stocks meeting both conditions
4. You review emails and decide whether to research/trade
5. No automation of actual trades; you maintain control

## Why This Approach?

### Simplicity

- One condition to watch (8% upside to MA200)
- Easy to understand and explain
- No complex multi-factor scoring

### Mechanical

- Removes emotion from screening
- Reproducible across time
- Auditable (you can verify calculations)

### Actionable

- Alerts aren't "interesting observations"—they're buy-level dips
- 8% upside threshold = worth your time to research
- No alert spam from minor price movements

### Conservative

- Waits for substantial dislocations (below MA200)
- Requires meaningful upside (8%+)
- Long-term averages (MA200, 1-year) = noise-resistant

## Customization Options

You can adjust the system via `config.py`:

```python
MIN_UPSIDE_FOR_ALERT = 8.0      # Change alert threshold (%)
MA200_PERIOD = 200              # Change MA200 length (days)
MA_1YEAR_PERIOD = 252           # Change 1-year avg length
MA_3MONTH_PERIOD = 63           # Change 3-month avg length
```

For example:
- More conservative? Set `MIN_UPSIDE_FOR_ALERT = 10.0`
- More aggressive? Set `MIN_UPSIDE_FOR_ALERT = 6.0`
- Shorter lookback? Set `MA200_PERIOD = 50` (50-day MA instead)

## Expected Outcomes

### When Will You Get Alerts?

- **Market downturns**: Most alerts (stocks sold off)
- **Individual stock weakness**: Sector-specific issues
- **After earnings misses**: Revenue/guidance disappointments
- **Temporary dislocations**: Algorithmic selling, sector rotation

### When Will You NOT Get Alerts?

- **Bull markets**: Stocks stay above their MAs
- **Recent IPOs/new stocks**: Insufficient history
- **Broken stocks**: Fundamentals deteriorating (stays below MA200 long-term)
- **Micro-caps**: Low liquidity, yfinance data gaps

### Expected Frequency

- **Market dependent**: 0-5+ alerts per week during downturns
- **Bull markets**: 0-1 alerts per week
- **Sideways markets**: 1-3 alerts per week

Adjust your watchlist size if too many or too few alerts.

## Limitations & Caveats

1. **Past performance**: MA200 is backward-looking, not predictive
2. **Technical only**: No fundamental analysis (by design—you add that)
3. **Price data only**: Ignores dividends, splits, corporate actions (minor impact)
4. **Timezone**: Uses market close times; adjust for your timezone if needed
5. **Gaps**: Long market holidays may skew calculations slightly

## Next Steps for Users

Once alerts arrive:

1. **Research**: Why did the stock dip? Is it temporary or structural?
2. **Fundamentals**: Is the company still healthy?
3. **Technicals**: Is there support around current levels?
4. **Position Size**: How much are you comfortable risking?
5. **Entry Plan**: Limit order? Scale in? Or wait longer?

The system identifies opportunities; your judgment executes them.

---

**Bottom Line**: This system is a scanner, not a recommendation engine. It mechanically identifies stocks trading at 8%+ discounts to their 200-day average, then gets out of the way so you can make informed decisions.
