"""Email service for sending Gmail alerts."""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Gmail SMTP settings
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587


def send_email(
    sender: str,
    app_password: str,
    recipient: str,
    subject: str,
    body_html: str
) -> bool:
    """
    Send an email via Gmail using app password.
    
    Args:
        sender: Gmail address sending the email
        app_password: Gmail app-specific password (NOT regular password)
        recipient: Email address to send to
        subject: Email subject line
        body_html: HTML body of the email
        
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        
        # Attach HTML body
        part = MIMEText(body_html, "html")
        msg.attach(part)
        
        # Send via Gmail SMTP
        with smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(sender, app_password)
            server.sendmail(sender, recipient, msg.as_string())
        
        logger.info(f"Email sent successfully to {recipient}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logger.error(
            "SMTP Authentication failed. Check Gmail address and app password."
        )
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False


def create_alert_email_html(
    ticker: str,
    current_price: float,
    ma200: float,
    ma_1year: float,
    ma_3month: float,
    upside_to_ma200: float,
    upside_to_1year: float,
    upside_to_3month: float,
    alert_level: str,
    company_name: Optional[str] = None
) -> str:
    """
    Create a professional HTML email for stock dip alert.
    
    Args:
        ticker: Stock ticker symbol
        current_price: Current stock price
        ma200: 200-day moving average
        ma_1year: 1-year average price
        ma_3month: 3-month average price
        upside_to_ma200: Upside to MA200 as percentage
        upside_to_1year: Upside to 1-year average as percentage
        upside_to_3month: Upside to 3-month average as percentage
        alert_level: Alert level classification
        company_name: Company name (optional)
        
    Returns:
        HTML string for email body
    """
    # Format alert level display
    level_icons = {
        "watch": "⚠️",
        "good_opportunity": "✅",
        "deep_discount": "🔥",
        "investigate_carefully": "🚨",
    }
    level_names = {
        "watch": "Watch (7-8% upside)",
        "good_opportunity": "Good Opportunity (8-12% upside)",
        "deep_discount": "Deep Discount (12-20% upside)",
        "investigate_carefully": "Investigate Carefully (20%+ upside)",
    }
    
    icon = level_icons.get(alert_level, "📊")
    level_name = level_names.get(alert_level, alert_level)
    company_display = f"{company_name} ({ticker})" if company_name else ticker
    
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 8px; border: 1px solid #ddd;">
          
          <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
            {icon} Stock Dip Alert
          </h2>
          
          <div style="background-color: #fff; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #e74c3c;">
            <h3 style="margin-top: 0; color: #e74c3c;">{company_display}</h3>
            <p style="margin: 5px 0;"><strong>Alert Level:</strong> {level_name}</p>
            <p style="margin: 5px 0;"><strong>Current Price:</strong> ${current_price:.2f}</p>
          </div>
          
          <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 15px 0;">
            <h4 style="margin-top: 0; color: #2c3e50;">Price Analysis</h4>
            <table style="width: 100%; border-collapse: collapse;">
              <tr style="border-bottom: 1px solid #bdc3c7;">
                <td style="padding: 8px; font-weight: bold;">Metric</td>
                <td style="padding: 8px; font-weight: bold;">Value</td>
                <td style="padding: 8px; font-weight: bold;">Upside</td>
              </tr>
              <tr style="border-bottom: 1px solid #bdc3c7;">
                <td style="padding: 8px;">200-Day MA</td>
                <td style="padding: 8px;">${ma200:.2f}</td>
                <td style="padding: 8px; color: #27ae60; font-weight: bold;">{upside_to_ma200:.2f}%</td>
              </tr>
              <tr style="border-bottom: 1px solid #bdc3c7;">
                <td style="padding: 8px;">1-Year Average</td>
                <td style="padding: 8px;">${ma_1year:.2f}</td>
                <td style="padding: 8px; color: #27ae60; font-weight: bold;">{upside_to_1year:.2f}%</td>
              </tr>
              <tr>
                <td style="padding: 8px;">3-Month Average</td>
                <td style="padding: 8px;">${ma_3month:.2f}</td>
                <td style="padding: 8px; color: #27ae60; font-weight: bold;">{upside_to_3month:.2f}%</td>
              </tr>
            </table>
          </div>
          
          <div style="background-color: #fff; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #27ae60;">
            <h4 style="margin-top: 0; color: #27ae60;">Summary</h4>
            <p>
              {ticker} is currently trading at <strong>${current_price:.2f}</strong>, which is 
              <strong>{abs(upside_to_ma200):.2f}% below</strong> its 200-day moving average of 
              <strong>${ma200:.2f}</strong>. If the stock returns to its 200-day average, 
              it could provide <strong>{upside_to_ma200:.2f}% upside</strong>.
            </p>
          </div>
          
          <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 15px 0; font-size: 12px; color: #555;">
            <p style="margin: 5px 0;">
              <strong>⏰ Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
            </p>
            <p style="margin: 5px 0;">
              This is an automated alert from your stock dip monitoring system.
            </p>
          </div>
          
        </div>
      </body>
    </html>
    """
    
    return html


def send_alert_email(
    sender: str,
    app_password: str,
    recipient: str,
    ticker: str,
    current_price: float,
    ma200: float,
    ma_1year: float,
    ma_3month: float,
    upside_to_ma200: float,
    upside_to_1year: float,
    upside_to_3month: float,
    alert_level: str,
    company_name: Optional[str] = None
) -> bool:
    """
    Send a formatted stock dip alert email.
    
    Args:
        sender: Gmail address
        app_password: Gmail app-specific password
        recipient: Email recipient
        ticker: Stock ticker symbol
        current_price: Current stock price
        ma200: 200-day moving average
        ma_1year: 1-year average price
        ma_3month: 3-month average price
        upside_to_ma200: Upside to MA200 as percentage
        upside_to_1year: Upside to 1-year average as percentage
        upside_to_3month: Upside to 3-month average as percentage
        alert_level: Alert level classification
        company_name: Company name (optional)
        
    Returns:
        True if email sent successfully, False otherwise
    """
    subject = f"Stock Dip Alert: {ticker} - {alert_level.replace('_', ' ').title()}"
    
    body_html = create_alert_email_html(
        ticker=ticker,
        current_price=current_price,
        ma200=ma200,
        ma_1year=ma_1year,
        ma_3month=ma_3month,
        upside_to_ma200=upside_to_ma200,
        upside_to_1year=upside_to_1year,
        upside_to_3month=upside_to_3month,
        alert_level=alert_level,
        company_name=company_name
    )
    
    return send_email(sender, app_password, recipient, subject, body_html)


def create_summary_email_html(alerts: List[dict]) -> str:
    """
    Create a summary HTML email with all alerts from a scan run.
    
    Args:
        alerts: List of alert dictionaries with keys: ticker, company_name,
          current_price, ma_alltime, ma200, ma_last_30_days,
          ma_last_quarter, week52_high, week52_low, week52_avg,
          upside_to_alltime, upside_to_ma200,
          upside_to_last_30_days, upside_to_last_quarter, 
          drop_from_week52_avg, alert_level, alert_source
        
    Returns:
        HTML string for email body
    """
    level_icons = {
        "watch": "⚠️",
        "good_opportunity": "✅",
        "deep_discount": "🔥",
        "investigate_carefully": "🚨",
    }
    level_names = {
        "watch": "Watch",
        "good_opportunity": "Good Opportunity",
        "deep_discount": "Deep Discount",
        "investigate_carefully": "Investigate Carefully",
    }
    
    alerts_html = ""
    for alert in alerts:
        ticker = alert["ticker"]
        company_name = alert.get("company_name") or ticker
        current_price = alert["current_price"]
        ma_alltime = alert["ma_alltime"]
        ma200 = alert["ma200"]
        ma_last_30_days = alert["ma_last_30_days"]
        ma_last_quarter = alert["ma_last_quarter"]
        week52_high = alert["week52_high"]
        week52_low = alert["week52_low"]
        week52_avg = alert["week52_avg"]
        upside_alltime = alert["upside_to_alltime"]
        upside_ma200 = alert["upside_to_ma200"]
        upside_last_30_days = alert["upside_to_last_30_days"]
        upside_last_quarter = alert["upside_to_last_quarter"]
        drop_from_52week = alert["drop_from_week52_avg"]
        level = alert["alert_level"]
        alert_source = alert["alert_source"]
        
        icon = level_icons.get(level, "📊")
        level_name = level_names.get(level, level)
        
        # Determine signal display
        signal_display = ""
        if alert_source == "both":
            signal_display = "🔔 DUAL SIGNAL (Historical + Forecast)"
        elif alert_source == "forecast":
            signal_display = "📈 Forecast Signal (52-week drop)"
        elif alert_source == "historical":
            signal_display = "📊 Historical Signal (MA200)"
        
        alerts_html += f"""
        <div style="background-color: #fff; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #e74c3c;">
          <h4 style="margin: 0 0 10px 0; color: #e74c3c;">
            {icon} {company_name} ({ticker})
          </h4>
          <p style="margin: 5px 0; font-size: 14px;">
            <strong>Alert Level:</strong> {level_name} | 
            <strong>Current Price:</strong> ${current_price:.2f} | 
            <strong>Signal:</strong> {signal_display}
          </p>
          
          <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px;">
            <tr style="border-bottom: 1px solid #ecf0f1; background-color: #f9f9f9;">
              <td style="padding: 8px; font-weight: bold;">Metric</td>
              <td style="padding: 8px; font-weight: bold;">Value</td>
              <td style="padding: 8px; font-weight: bold;">Upside/Drop</td>
            </tr>
            <tr style="border-bottom: 1px solid #ecf0f1;">
              <td style="padding: 8px;">All-Time Average</td>
              <td style="padding: 8px;">${ma_alltime:.2f}</td>
              <td style="padding: 8px; color: #27ae60; font-weight: bold;">{upside_alltime:.2f}%</td>
            </tr>
            <tr style="border-bottom: 1px solid #ecf0f1;">
              <td style="padding: 8px;">200-Day MA</td>
              <td style="padding: 8px;">${ma200:.2f}</td>
              <td style="padding: 8px; color: #27ae60; font-weight: bold;">{upside_ma200:.2f}%</td>
            </tr>
            <tr style="border-bottom: 1px solid #ecf0f1;">
              <td style="padding: 8px;">Last 30 Days Average</td>
              <td style="padding: 8px;">${ma_last_30_days:.2f}</td>
              <td style="padding: 8px; color: #27ae60; font-weight: bold;">{upside_last_30_days:.2f}%</td>
            </tr>
            <tr style="border-bottom: 1px solid #ecf0f1;">
              <td style="padding: 8px;">Last Quarter Average</td>
              <td style="padding: 8px;">${ma_last_quarter:.2f}</td>
              <td style="padding: 8px; color: #27ae60; font-weight: bold;">{upside_last_quarter:.2f}%</td>
            </tr>
            <tr style="border-bottom: 1px solid #ecf0f1; background-color: #fef9e7;">
              <td style="padding: 8px; font-weight: bold;">52-Week High</td>
              <td style="padding: 8px; font-weight: bold;">${week52_high:.2f}</td>
              <td style="padding: 8px; color: #d35400; font-weight: bold;">Peak</td>
            </tr>
            <tr style="border-bottom: 1px solid #ecf0f1; background-color: #fef9e7;">
              <td style="padding: 8px; font-weight: bold;">52-Week Average</td>
              <td style="padding: 8px; font-weight: bold;">${week52_avg:.2f}</td>
              <td style="padding: 8px; color: #d35400; font-weight: bold;">{drop_from_52week:.2f}%</td>
            </tr>
            <tr style="background-color: #fef9e7;">
              <td style="padding: 8px; font-weight: bold;">52-Week Low</td>
              <td style="padding: 8px; font-weight: bold;">${week52_low:.2f}</td>
              <td style="padding: 8px; color: #d35400; font-weight: bold;">Floor</td>
            </tr>
          </table>
        </div>
        """
    
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 700px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 8px; border: 1px solid #ddd;">
          
          <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
            📊 Stock Dip Alert Summary
          </h2>
          
          <p style="background-color: #ecf0f1; padding: 10px; border-radius: 5px; margin: 15px 0;">
            <strong>Scan Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC<br>
            <strong>Alerts Found:</strong> {len(alerts)}
          </p>
          
          <div style="margin: 20px 0;">
            {alerts_html}
          </div>
          
          <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 15px 0; font-size: 12px; color: #555;">
            <p style="margin: 5px 0;">
              This is an automated summary from your stock dip monitoring system.
            </p>
          </div>
          
        </div>
      </body>
    </html>
    """
    
    return html


def send_summary_email(
    sender: str,
    app_password: str,
    recipient: str,
    alerts: List[dict]
) -> bool:
    """
    Send a summary email with all alerts from a scan run.
    
    Args:
        sender: Gmail address
        app_password: Gmail app-specific password
        recipient: Email recipient
        alerts: List of alert dictionaries
        
    Returns:
        True if email sent successfully, False otherwise
    """
    if not alerts:
        logger.info("No alerts to send")
        return True
    
    subject = f"Stock Dip Alert Summary - {len(alerts)} Opportunities"
    body_html = create_summary_email_html(alerts)
    
    return send_email(sender, app_password, recipient, subject, body_html)
