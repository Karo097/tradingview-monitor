#!/usr/bin/env python3
"""
Simple test for hourly email system
"""

from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_hourly_system():
    print("TESTING HOURLY EMAIL SYSTEM")
    print("=" * 50)
    
    now = datetime.now()
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current minute: {now.minute}")
    
    # Test if it's 42 minutes past the hour
    if now.minute == 42:
        print("It's currently 42 minutes past the hour!")
        print("Email should be sent NOW!")
    else:
        print(f"It's {now.minute} minutes past the hour")
        print("Email will be sent at 42 minutes past the hour")
    
    # Show next email times
    print("\nNEXT EMAIL TIMES:")
    for i in range(24):
        next_time = now.replace(minute=42, second=0, microsecond=0) + timedelta(hours=i)
        if next_time > now:
            print(f"   {next_time.strftime('%Y-%m-%d %H:%M')}")
            if i >= 5:  # Show next 5 times
                break

def send_test_email():
    try:
        now = datetime.now()
        
        # Email configuration
        sender_email = "karo.jihad@gmail.com"
        recipient_email = "karo.jihad@gmail.com"
        password = "mlmo swho bdgp kadg"
        
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

SELLER STATUS: TESTING
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
    test_hourly_system()
    print("\n" + "="*50)
    print("Sending test hourly email...")
    send_test_email()
