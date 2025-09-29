#!/usr/bin/env python3
"""
Check system status and debug missing notifications
"""
import requests
import json
from datetime import datetime

def check_render_service():
    """Check if Render.com service is running"""
    try:
        print("Checking Render.com service...")
        response = requests.get('https://tradingview-monitor.onrender.com/status', timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Service Response: {data}")
            
            # Check last check time
            last_check = data.get('last_check', '')
            if last_check:
                print(f"Last Check: {last_check}")
                
                # Parse timestamp
                try:
                    last_time = datetime.strptime(last_check, '%Y-%m-%d %H:%M:%S')
                    now = datetime.now()
                    diff = now - last_time
                    
                    print(f"Time since last check: {diff}")
                    
                    if diff.total_seconds() > 3600:  # More than 1 hour
                        print("WARNING: Service hasn't checked in over 1 hour!")
                        print("The monitoring loop might be broken or sleeping.")
                    else:
                        print("Service is checking regularly.")
                        
                except Exception as e:
                    print(f"Error parsing timestamp: {e}")
            
            return True, data
        else:
            print(f"Service Error: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"Connection Error: {e}")
        return False, None

def check_monitoring_log():
    """Check the monitoring log"""
    try:
        print("\nChecking monitoring log...")
        response = requests.get('https://tradingview-monitor.onrender.com/monitoring-log', timeout=15)
        print(f"Log Status: {response.status_code}")
        
        if response.status_code == 200:
            log_data = response.json()
            print(f"Log Data: {log_data}")
            return True
        else:
            print(f"Log Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Log check error: {e}")
        return False

def test_telegram_now():
    """Test Telegram bot right now"""
    try:
        print("\nTesting Telegram bot...")
        
        # Test the Telegram bot directly
        bot_token = "7405449740:AAFWd4zQYqr8JyRTPB5jQ0oPV_D00ep28Ms"
        chat_id = 780489145
        
        test_message = f"TEST: System check at {datetime.now().strftime('%H:%M:%S')}"
        
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": test_message
        }
        
        response = requests.post(telegram_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("Telegram bot test: SUCCESS")
            return True
        else:
            print(f"Telegram bot test: FAILED - {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Telegram test error: {e}")
        return False

def check_current_time():
    """Check current time and next expected notification"""
    now = datetime.now()
    current_minute = now.minute
    current_hour = now.hour
    
    print(f"\nCurrent Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current Hour: {current_hour}")
    print(f"Current Minute: {current_minute}")
    
    # Calculate next 42-minute mark
    if current_minute < 42:
        next_42 = now.replace(minute=42, second=0, microsecond=0)
    else:
        next_42 = now.replace(hour=current_hour + 1, minute=42, second=0, microsecond=0)
    
    print(f"Next expected notification: {next_42.strftime('%H:%M')}")
    
    # Check if we missed any notifications
    if current_minute > 42:
        missed_time = now.replace(minute=42, second=0, microsecond=0)
        print(f"Missed notification should have been at: {missed_time.strftime('%H:%M')}")

def main():
    print("TradingView Monitor System Check")
    print("=" * 50)
    print(f"Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check current time
    check_current_time()
    
    # Check service
    service_ok, service_data = check_render_service()
    log_ok = check_monitoring_log()
    
    # Test Telegram
    telegram_ok = test_telegram_now()
    
    print("\nDIAGNOSTIC SUMMARY:")
    print(f"Service Status: {'OK' if service_ok else 'FAILED'}")
    print(f"Log Access: {'OK' if log_ok else 'FAILED'}")
    print(f"Telegram Bot: {'OK' if telegram_ok else 'FAILED'}")
    
    if service_ok and service_data:
        last_check = service_data.get('last_check', '')
        if last_check:
            try:
                last_time = datetime.strptime(last_check, '%Y-%m-%d %H:%M:%S')
                now = datetime.now()
                diff = now - last_time
                
                if diff.total_seconds() > 3600:
                    print("\nISSUE IDENTIFIED:")
                    print("- Service is not checking regularly")
                    print("- Monitoring loop might be broken")
                    print("- Render.com might have put the service to sleep")
                else:
                    print("\nSERVICE IS WORKING:")
                    print("- Regular checks are happening")
                    print("- Issue might be with notification timing")
                    
            except Exception as e:
                print(f"Error analyzing timestamps: {e}")
    
    print("\nRECOMMENDATIONS:")
    if not service_ok:
        print("1. Render.com service is down - check deployment")
    elif not telegram_ok:
        print("1. Telegram bot is not working - check credentials")
    else:
        print("1. System appears to be working")
        print("2. Check if notifications are being sent at the right time")
        print("3. Check Render.com logs for any errors")

if __name__ == "__main__":
    main()
