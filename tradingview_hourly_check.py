#!/usr/bin/env python3
"""
Simple TradingView Hourly Checker
Checks seller status and sends Telegram notification
Designed to be called by cloud cron services
"""

import requests
import json
import re
import html
from datetime import datetime
from email_notifier import EmailNotifier

def check_seller_status():
    """Check if seller is online and get fresh cookies"""
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking seller status...")
        
        url = "https://www.oxaam.com/tradecookienew45.php?key=WH87A345N94WDLY"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            content = response.text
            
            # Check if seller is online
            if "Validity Remaining" in content:
                print("Seller is ONLINE - Fresh cookies available!")
                
                # Extract cookies
                json_pattern = r'\[.*?\]'
                matches = re.findall(json_pattern, content, re.DOTALL)
                
                if matches:
                    try:
                        decoded = html.unescape(matches[0])
                        cookies = json.loads(decoded)
                        
                        # Save cookies
                        save_cookies(cookies)
                        
                        return True, f"Seller is ONLINE! {len(cookies)} fresh cookies available", cookies
                    except Exception as e:
                        print(f"Error parsing cookies: {e}")
                        return True, "Seller is ONLINE but cookies parsing failed", None
                else:
                    return True, "Seller is ONLINE but no cookies found", None
            else:
                print("Seller is OFFLINE - No fresh cookies")
                return False, "Seller is OFFLINE - No fresh cookies available", None
        else:
            print(f"HTTP Error: {response.status_code}")
            return False, f"HTTP Error: {response.status_code}", None
            
    except Exception as e:
        print(f"Error checking seller: {e}")
        return False, f"Error: {e}", None

def save_cookies(cookies):
    """Save cookies to file"""
    try:
        with open('tradingview_cookies.json', 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"Saved {len(cookies)} cookies to tradingview_cookies.json")
    except Exception as e:
        print(f"Error saving cookies: {e}")

def load_last_cookies():
    """Load last saved cookies"""
    try:
        with open('tradingview_cookies.json', 'r') as f:
            cookies = json.load(f)
        return cookies
    except:
        return None

def send_hourly_notification(is_online, message, fresh_cookies):
    """Send hourly notification via Telegram"""
    try:
        notifier = EmailNotifier()
        
        # Prepare notification
        current_time = datetime.now()
        subject = f"TradingView Hourly Report - {current_time.strftime('%H:%M')}"
        
        if is_online and fresh_cookies:
            # Seller is online with fresh cookies - send shorter message
            notification_message = f"""TradingView Hourly Report - {current_time.strftime('%H:%M')}

Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
Status: {message}
Cookies: {len(fresh_cookies)} fresh cookies available

SELLER STATUS: ONLINE ✅

Fresh cookies are available and saved to file.
Download: https://tradingview-monitor.onrender.com/download-browser-import

Next update: {(current_time.replace(minute=42, second=0, microsecond=0) + timedelta(hours=1)).strftime('%H:%M')}
"""
        else:
            # Seller is offline - send shorter message
            last_cookies = load_last_cookies()
            if last_cookies:
                cookies_info = f"{len(last_cookies)} last saved cookies"
            else:
                cookies_info = "No cookies available"
            
            notification_message = f"""TradingView Hourly Report - {current_time.strftime('%H:%M')} (OFFLINE)

Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
Status: {message}

SELLER STATUS: OFFLINE ⏳

No fresh cookies available at this time.
Last saved: {cookies_info}

The system continues monitoring and will notify you when the seller comes back online.

Next update: {(current_time.replace(minute=42, second=0, microsecond=0) + timedelta(hours=1)).strftime('%H:%M')}
"""
        
        # Send notification
        success = notifier.send_notification(subject, notification_message)
        
        if success:
            print("Hourly notification sent successfully!")
        else:
            print("Failed to send notification")
            
        return success
        
    except Exception as e:
        print(f"Error sending notification: {e}")
        return False

def main():
    """Main function - check seller and send notification"""
    print("=" * 50)
    print("TradingView Hourly Check")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Check seller status
    is_online, message, fresh_cookies = check_seller_status()
    
    # Send notification
    send_hourly_notification(is_online, message, fresh_cookies)
    
    print("=" * 50)
    print("Hourly check completed!")
    print("=" * 50)

if __name__ == "__main__":
    from datetime import timedelta
    main()
