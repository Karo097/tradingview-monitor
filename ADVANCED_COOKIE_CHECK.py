#!/usr/bin/env python3
"""
Advanced cookie checker that tests cookies by actually trying to access TradingView
"""

import requests
import json
import os
import glob
from datetime import datetime

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = "7405449740:AAFWd4zQYqr8JyRTPB5jQ0oPV_D00ep28Ms"
TELEGRAM_CHAT_ID = 780489145
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_telegram_message(message):
    """Send message via Telegram"""
    try:
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        
        response = requests.post(
            TELEGRAM_URL,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"Telegram message sent successfully")
            return True
        else:
            print(f"Telegram failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False

def test_cookies_advanced(cookies):
    """Advanced test to check if cookies actually work with TradingView"""
    try:
        session = requests.Session()
        
        # Add cookies to session
        for cookie in cookies:
            session.cookies.set(
                cookie['name'], 
                cookie['value'],
                domain=cookie.get('domain', '.tradingview.com'),
                path=cookie.get('path', '/')
            )
        
        # Test multiple TradingView pages
        test_urls = [
            ("https://www.tradingview.com/", "Main page"),
            ("https://www.tradingview.com/chart/", "Chart page"),
            ("https://www.tradingview.com/accounts/", "Account page"),
            ("https://www.tradingview.com/screener/", "Screener page")
        ]
        
        working_pages = []
        failed_pages = []
        
        for url, description in test_urls:
            try:
                response = session.get(url, timeout=15)
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    # Check for signs of successful login
                    login_indicators = [
                        'logout', 'sign out', 'account', 'profile',
                        'premium', 'pro', 'advanced', 'real-time',
                        'watchlist', 'alerts', 'publish'
                    ]
                    
                    found_indicators = []
                    for indicator in login_indicators:
                        if indicator in content:
                            found_indicators.append(indicator)
                    
                    if found_indicators:
                        working_pages.append(f"{description}: {', '.join(found_indicators[:3])}")
                    else:
                        # Check if it's a login page
                        if 'sign in' in content or 'login' in content:
                            failed_pages.append(f"{description}: Login required")
                        else:
                            failed_pages.append(f"{description}: No login indicators")
                            
                else:
                    failed_pages.append(f"{description}: HTTP {response.status_code}")
                    
            except Exception as e:
                failed_pages.append(f"{description}: Error - {str(e)[:50]}")
        
        # Determine overall status
        if len(working_pages) >= 2:
            return True, f"Working on {len(working_pages)} pages: {working_pages[0]}"
        elif len(working_pages) == 1:
            return True, f"Partially working: {working_pages[0]}"
        else:
            return False, f"Not working: {failed_pages[0] if failed_pages else 'No response'}"
            
    except Exception as e:
        return False, f"Error testing cookies: {e}"

def main():
    """Main function"""
    print("Advanced Cookie Test - Sending to Telegram")
    print("=" * 50)
    
    # Look for cookie files
    pattern = "tradingview_cookies*.json"
    cookie_files = glob.glob(pattern)
    cookie_files.sort(key=os.path.getmtime, reverse=True)
    
    print(f"Found {len(cookie_files)} cookie files")
    
    if not cookie_files:
        message = "No cookie files found. Run the hourly check first to generate some cookies."
        send_telegram_message(message)
        return
    
    # Check last 5 files (or all available if less than 5)
    files_to_check = cookie_files[:5]
    
    working_cookies = []
    failed_cookies = []
    
    for i, file_path in enumerate(files_to_check, 1):
        try:
            print(f"Testing file {i}/{len(files_to_check)}: {file_path}")
            
            # Load cookies from file
            with open(file_path, 'r') as f:
                cookies = json.load(f)
            
            # Test cookies with advanced method
            is_working, message = test_cookies_advanced(cookies)
            
            file_info = {
                'file': os.path.basename(file_path),
                'cookies_count': len(cookies),
                'timestamp': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                'message': message
            }
            
            if is_working:
                working_cookies.append(file_info)
                print(f"WORKING: {file_path}")
            else:
                failed_cookies.append(file_info)
                print(f"FAILED: {file_path}")
                
        except Exception as e:
            print(f"Error checking {file_path}: {e}")
            failed_cookies.append({
                'file': os.path.basename(file_path),
                'error': str(e)
            })
    
    # Prepare response
    response = f"ADVANCED COOKIE TEST - Last {len(files_to_check)} files\n\n"
    
    if working_cookies:
        response += f"WORKING COOKIES ({len(working_cookies)}):\n"
        for cookie in working_cookies:
            response += f"- {cookie['file']} ({cookie['cookies_count']} cookies) - {cookie['timestamp']}\n"
            response += f"  Status: {cookie['message']}\n\n"
    else:
        response += "NO WORKING COOKIES FOUND\n\n"
    
    if failed_cookies:
        response += f"FAILED COOKIES ({len(failed_cookies)}):\n"
        for cookie in failed_cookies:
            if 'error' in cookie:
                response += f"- {cookie['file']} - Error: {cookie['error']}\n"
            else:
                response += f"- {cookie['file']} - {cookie['message']}\n"
    
    response += f"\nSUMMARY:\n"
    response += f"- Total checked: {len(files_to_check)}\n"
    response += f"- Working: {len(working_cookies)}\n"
    response += f"- Failed: {len(failed_cookies)}\n"
    
    if working_cookies:
        response += f"\nRECOMMENDATION: Use the most recent working cookie file:\n"
        response += f"{working_cookies[0]['file']}\n"
        response += f"{working_cookies[0]['timestamp']}\n"
        response += f"\nThis cookie has been tested and works with TradingView!"
    else:
        response += f"\nWARNING: No working cookies found. The seller might be offline or cookies have expired.\n"
        response += f"Try running the hourly check again or wait for the seller to come back online.\n"
    
    print("\nSending to Telegram...")
    print(response)
    
    success = send_telegram_message(response)
    
    if success:
        print("Message sent to Telegram successfully!")
    else:
        print("Failed to send message to Telegram")

if __name__ == "__main__":
    main()
