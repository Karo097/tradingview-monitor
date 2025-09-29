#!/usr/bin/env python3
"""
Deep analysis of the Telegram bot notification system
"""
import requests
import json
from datetime import datetime
import time

def test_telegram_directly():
    """Test Telegram bot with detailed logging"""
    print("=== TELEGRAM BOT DIRECT TEST ===")
    
    bot_token = "7405449740:AAFWd4zQYqr8JyRTPB5jQ0oPV_D00ep28Ms"
    chat_id = 780489145
    
    # Test 1: Basic message
    print("Test 1: Basic message")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": f"DEEP TEST 1: {datetime.now().strftime('%H:%M:%S')}"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("SUCCESS: Basic message sent")
        else:
            print("FAILED: Basic message")
            
    except Exception as e:
        print(f"ERROR: Basic message error: {e}")
    
    # Test 2: Message with formatting
    print("\nTest 2: Message with formatting")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": f"*DEEP TEST 2*: {datetime.now().strftime('%H:%M:%S')}",
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("SUCCESS: Formatted message sent")
        else:
            print("FAILED: Formatted message")
            
    except Exception as e:
        print(f"ERROR: Formatted message error: {e}")
    
    # Test 3: Long message (like our notifications)
    print("\nTest 3: Long notification message")
    try:
        long_message = f"""TradingView Hourly Status Report

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: Seller is ONLINE! 3 critical cookies present
Cookies Saved: 16 cookies

SELLER STATUS: ONLINE
Fresh cookies are available and automatically saved!

FRESH COOKIES (JSON FORMAT):
[{{"domain": ".tradingview.com", "name": "sessionid", "value": "test123"}}]

You can:
1. Copy the JSON above and import to your browser
2. Download fresh cookies: https://tradingview-monitor.onrender.com/download-browser-import
3. Access premium TradingView features

This is your hourly update (sent at 42 minutes past each hour).
Next update: {(datetime.now().replace(minute=42, second=0, microsecond=0) + timedelta(hours=1)).strftime('%H:%M')}
"""
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": long_message
        }
        
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("SUCCESS: Long message sent")
        else:
            print("FAILED: Long message")
            
    except Exception as e:
        print(f"ERROR: Long message error: {e}")

def test_email_notifier_class():
    """Test the EmailNotifier class directly"""
    print("\n=== EMAIL NOTIFIER CLASS TEST ===")
    
    try:
        from email_notifier import EmailNotifier
        
        notifier = EmailNotifier()
        print(f"Bot Token: {notifier.telegram_bot_token[:20]}...")
        print(f"Chat ID: {notifier.telegram_chat_id}")
        print(f"Telegram URL: {notifier.telegram_url}")
        
        # Test the send_notification method
        result = notifier.send_notification(
            "DEEP TEST: EmailNotifier Class",
            f"This is a test from the EmailNotifier class at {datetime.now().strftime('%H:%M:%S')}"
        )
        
        print(f"Send notification result: {result}")
        
    except Exception as e:
        print(f"ERROR: EmailNotifier class error: {e}")

def check_render_service_detailed():
    """Check Render.com service with detailed analysis"""
    print("\n=== RENDER.COM SERVICE DETAILED CHECK ===")
    
    try:
        # Check main page
        response = requests.get('https://tradingview-monitor.onrender.com/', timeout=15)
        print(f"Main page status: {response.status_code}")
        
        if "v2.0" in response.text:
            print("SUCCESS: Latest code is deployed (v2.0)")
        else:
            print("WARNING: Old code is still running")
        
        # Check status endpoint
        response = requests.get('https://tradingview-monitor.onrender.com/status', timeout=15)
        print(f"Status endpoint: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Status data: {data}")
            
            # Check if monitoring is active
            last_check = data.get('last_check', '')
            if last_check:
                try:
                    last_time = datetime.strptime(last_check, '%Y-%m-%d %H:%M:%S')
                    now = datetime.now()
                    diff = now - last_time
                    
                    print(f"Last check: {last_check}")
                    print(f"Time since last check: {diff}")
                    
                    if diff.total_seconds() > 3600:
                        print("WARNING: Service hasn't checked in over 1 hour")
                    else:
                        print("SUCCESS: Service is checking regularly")
                        
                except Exception as e:
                    print(f"Error parsing timestamp: {e}")
        
        # Check monitoring log
        response = requests.get('https://tradingview-monitor.onrender.com/monitoring-log', timeout=15)
        print(f"Monitoring log: {response.status_code}")
        
        if response.status_code == 200:
            log_data = response.json()
            print(f"Log entries: {len(log_data.get('log', '').split('\\n'))}")
            print(f"Last log entry: {log_data.get('log', '')[-200:]}")
        
    except Exception as e:
        print(f"ERROR: Render.com service error: {e}")

def analyze_monitoring_timing():
    """Analyze the monitoring timing logic"""
    print("\n=== MONITORING TIMING ANALYSIS ===")
    
    now = datetime.now()
    current_minute = now.minute
    current_hour = now.hour
    
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current hour: {current_hour}")
    print(f"Current minute: {current_minute}")
    
    # Check if it's 42 minutes past the hour
    if current_minute == 42:
        print("SUCCESS: It's exactly 42 minutes past the hour - should be checking now!")
    elif current_minute < 42:
        print(f"WAITING: {42 - current_minute} minutes until next check")
    else:
        print(f"WAITING: {60 - current_minute + 42} minutes until next check")
    
    # Calculate next 42-minute mark
    if current_minute < 42:
        next_42 = now.replace(minute=42, second=0, microsecond=0)
    else:
        next_42 = now.replace(hour=current_hour + 1, minute=42, second=0, microsecond=0)
    
    print(f"Next check should be at: {next_42.strftime('%H:%M')}")
    
    # Check recent 42-minute marks
    print("\nRecent 42-minute marks:")
    for i in range(5):
        check_time = now.replace(minute=42, second=0, microsecond=0) - timedelta(hours=i)
        if check_time <= now:
            print(f"  {check_time.strftime('%H:%M')} - {'MISSED' if check_time < now - timedelta(minutes=10) else 'RECENT'}")

def main():
    print("DEEP TELEGRAM BOT ANALYSIS")
    print("=" * 60)
    print(f"Analysis time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test Telegram directly
    test_telegram_directly()
    
    # Test EmailNotifier class
    test_email_notifier_class()
    
    # Check Render.com service
    check_render_service_detailed()
    
    # Analyze timing
    analyze_monitoring_timing()
    
    print("\n" + "=" * 60)
    print("DEEP ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    from datetime import timedelta
    main()
