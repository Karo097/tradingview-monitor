#!/usr/bin/env python3
"""
Test the hourly email system
"""

from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_hourly_email_logic():
    """Test the hourly email logic"""
    print("TESTING HOURLY EMAIL SYSTEM")
    print("=" * 50)
    
    # Simulate the should_send_hourly_email logic
    def should_send_hourly_email(last_email_sent=None):
        now = datetime.now()
        current_minute = now.minute
        
        # Check if it's exactly 42 minutes past the hour
        if current_minute == 42:
            # Check if we already sent an email this hour
            if last_email_sent is None:
                return True
            
            # Check if the last email was sent in a different hour
            last_hour = last_email_sent.hour
            current_hour = now.hour
            
            # If it's a new hour (or new day), send email
            if current_hour != last_hour:
                return True
        
        return False
    
    # Test different scenarios
    now = datetime.now()
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current minute: {now.minute}")
    
    # Test if it's 42 minutes past the hour
    if now.minute == 42:
        print("✅ It's currently 42 minutes past the hour!")
        print("✅ Email should be sent NOW!")
    else:
        print(f"⏰ It's {now.minute} minutes past the hour")
        print("⏰ Email will be sent at 42 minutes past the hour")
    
    # Show next email times
    print("\n📅 NEXT EMAIL TIMES:")
    for i in range(24):
        next_time = now.replace(minute=42, second=0, microsecond=0) + timedelta(hours=i)
        if next_time > now:
            print(f"   {next_time.strftime('%Y-%m-%d %H:%M')}")
            if i >= 5:  # Show next 5 times
                break

def send_test_hourly_email():
    """Send a test hourly email"""
    try:
        now = datetime.now()
        
        # Email configuration
        sender_email = "karo.jihad@gmail.com"
        recipient_email = "karo.jihad@gmail.com"
        password = "mlmo swho bdgp kadg"  # App password
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"TEST: TradingView Hourly Report - {now.strftime('%H:%M')}"
        
        # Test message
        email_message = f"""
TEST: TradingView Hourly Status Report

Time: {now.strftime('%Y-%m-%d %H:%M:%S')}
Status: TEST EMAIL - Hourly system is working!

SELLER STATUS: TESTING ✅
This is a test email to verify the hourly email system.

The system will now send you emails every hour at 42 minutes past each hour:
- 00:42, 01:42, 02:42, 03:42, etc.
- 24 emails per day total

Next real email: {(now.replace(minute=42, second=0, microsecond=0) + timedelta(hours=1)).strftime('%H:%M')}

This is your hourly update (sent at 42 minutes past each hour).
"""
        
        msg.attach(MIMEText(email_message, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("SUCCESS: Test hourly email sent to karo.jihad@gmail.com")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to send test email - {e}")
        return False

if __name__ == "__main__":
    test_hourly_email_logic()
    print("\n" + "="*50)
    print("Sending test hourly email...")
    send_test_hourly_email()
