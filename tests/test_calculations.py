"""Unit tests for calculation functions."""

import unittest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from calculations import (
    calculate_upside_percentage,
    classify_alert_level,
    should_alert,
    analyze_stock,
)


class TestUpsideCalculation(unittest.TestCase):
    """Test upside percentage calculations."""
    
    def test_upside_basic(self):
        """Test basic upside calculation."""
        # Current: $100, Target: $110 = 10% upside
        result = calculate_upside_percentage(100, 110)
        self.assertAlmostEqual(result, 10.0, places=2)
    
    def test_upside_with_decimals(self):
        """Test upside calculation with decimal prices."""
        # Current: $150.50, Target: $162.54 = ~7.99% upside
        result = calculate_upside_percentage(150.50, 162.54)
        self.assertAlmostEqual(result, 7.99, places=1)
    
    def test_downside_negative(self):
        """Test that downside results in negative percentage."""
        # Current: $100, Target: $90 = -10% (downside)
        result = calculate_upside_percentage(100, 90)
        self.assertAlmostEqual(result, -10.0, places=2)
    
    def test_no_change(self):
        """Test when current equals target."""
        result = calculate_upside_percentage(100, 100)
        self.assertEqual(result, 0.0)
    
    def test_zero_current_price(self):
        """Test edge case of zero current price."""
        result = calculate_upside_percentage(0, 100)
        self.assertEqual(result, 0.0)


class TestAlertClassification(unittest.TestCase):
    """Test alert level classification."""
    
    def test_watch_level(self):
        """Test 'watch' level (7-8%)."""
        result = classify_alert_level(7.5)
        self.assertEqual(result, "watch")
    
    def test_good_opportunity_level(self):
        """Test 'good_opportunity' level (8-12%)."""
        result = classify_alert_level(10.0)
        self.assertEqual(result, "good_opportunity")
    
    def test_deep_discount_level(self):
        """Test 'deep_discount' level (12-20%)."""
        result = classify_alert_level(15.0)
        self.assertEqual(result, "deep_discount")
    
    def test_investigate_carefully_level(self):
        """Test 'investigate_carefully' level (20%+)."""
        result = classify_alert_level(25.0)
        self.assertEqual(result, "investigate_carefully")
    
    def test_no_alert_below_threshold(self):
        """Test 'no_alert' when below 7%."""
        result = classify_alert_level(6.5)
        self.assertEqual(result, "no_alert")
    
    def test_boundary_8_percent(self):
        """Test boundary at 8%."""
        result = classify_alert_level(8.0)
        self.assertEqual(result, "good_opportunity")
    
    def test_boundary_12_percent(self):
        """Test boundary at 12%."""
        result = classify_alert_level(12.0)
        self.assertEqual(result, "deep_discount")
    
    def test_boundary_20_percent(self):
        """Test boundary at 20%."""
        result = classify_alert_level(20.0)
        self.assertEqual(result, "investigate_carefully")


class TestAlertLogic(unittest.TestCase):
    """Test alert triggering logic."""
    
    def test_should_alert_below_ma200_sufficient_upside(self):
        """Test alert triggers when below MA200 with sufficient upside."""
        # Stock at $90, MA200 at $100, upside 11%
        result = should_alert(
            current_price=90,
            ma200=100,
            upside_to_ma200=11.0,
            min_upside_threshold=8.0
        )
        self.assertTrue(result)
    
    def test_no_alert_above_ma200(self):
        """Test no alert when above MA200."""
        result = should_alert(
            current_price=110,
            ma200=100,
            upside_to_ma200=-10.0,
            min_upside_threshold=8.0
        )
        self.assertFalse(result)
    
    def test_no_alert_below_ma200_insufficient_upside(self):
        """Test no alert when below MA200 but upside < threshold."""
        # Stock at $95, MA200 at $100, upside 5%
        result = should_alert(
            current_price=95,
            ma200=100,
            upside_to_ma200=5.0,
            min_upside_threshold=8.0
        )
        self.assertFalse(result)
    
    def test_alert_at_exact_threshold(self):
        """Test alert triggers at exact threshold."""
        result = should_alert(
            current_price=92.6,
            ma200=100,
            upside_to_ma200=8.0,
            min_upside_threshold=8.0
        )
        self.assertTrue(result)


class TestStockAnalysis(unittest.TestCase):
    """Test comprehensive stock analysis."""
    
    def test_analyze_stock_with_alert(self):
        """Test stock analysis that triggers an alert."""
        result = analyze_stock(
            ticker="AAPL",
            current_price=90.0,
            ma_alltime=92.0,
            ma200=100.0,
            ma_last_30_days=94.0,
            ma_last_quarter=96.0,
            min_upside_threshold=8.0
        )
        
        # Verify structure
        self.assertIn("ticker", result)
        self.assertIn("current_price", result)
        self.assertIn("alert_triggered", result)
        self.assertIn("alert_level", result)
        
        # Verify values
        self.assertEqual(result["ticker"], "AAPL")
        self.assertEqual(result["current_price"], 90.0)
        self.assertTrue(result["alert_triggered"])
        self.assertEqual(result["alert_level"], "good_opportunity")
    
    def test_analyze_stock_no_alert(self):
        """Test stock analysis with no alert."""
        result = analyze_stock(
            ticker="MSFT",
            current_price=110.0,
            ma_alltime=108.0,
            ma200=100.0,
            ma_last_30_days=107.0,
            ma_last_quarter=109.0,
            min_upside_threshold=8.0
        )
        
        self.assertFalse(result["alert_triggered"])
        self.assertEqual(result["alert_level"], "no_alert")
    
    def test_analyze_stock_deep_discount(self):
        """Test stock analysis with deep discount."""
        result = analyze_stock(
            ticker="GOOGL",
            current_price=80.0,
            ma_alltime=85.0,
            ma200=100.0,
            ma_last_30_days=88.0,
            ma_last_quarter=89.0,
            min_upside_threshold=8.0
        )
        
        self.assertTrue(result["alert_triggered"])
        self.assertEqual(result["alert_level"], "investigate_carefully")
        self.assertAlmostEqual(result["upside_to_ma200"], 25.0, places=1)
    
    def test_analyze_stock_rounding(self):
        """Test that prices are properly rounded."""
        result = analyze_stock(
            ticker="TSLA",
            current_price=100.123456,
            ma_alltime=180.234567,
            ma200=200.987654,
            ma_last_30_days=140.555555,
            ma_last_quarter=120.111111,
            min_upside_threshold=8.0
        )
        
        # Verify rounding to 2 decimal places
        self.assertEqual(result["current_price"], 100.12)
        self.assertEqual(result["ma_alltime"], 180.23)
        self.assertEqual(result["ma200"], 200.99)
        self.assertEqual(result["ma_last_30_days"], 140.56)
        self.assertEqual(result["ma_last_quarter"], 120.11)


if __name__ == "__main__":
    unittest.main()
