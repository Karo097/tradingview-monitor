#!/usr/bin/env python3
"""
Interactive Cookie Checker
Allows you to specify how many cookies to check and provides working cookie files
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
        
        # Test TradingView pages
        test_urls = [
            ("https://www.tradingview.com/", "Main page"),
            ("https://www.tradingview.com/chart/", "Chart page"),
            ("https://www.tradingview.com/accounts/", "Account page")
        ]
        
        working_pages = []
        
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
                        working_pages.append(f"{description}: {', '.join(found_indicators[:2])}")
                            
            except Exception as e:
                continue
        
        # Determine overall status
        if len(working_pages) >= 2:
            return True, f"Working on {len(working_pages)} pages: {working_pages[0]}"
        elif len(working_pages) == 1:
            return True, f"Partially working: {working_pages[0]}"
        else:
            return False, "Not working: No login indicators found"
            
    except Exception as e:
        return False, f"Error testing cookies: {e}"

def save_working_cookies(working_cookies, filename_prefix="working_cookies"):
    """Save working cookies to a file"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{filename_prefix}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(working_cookies, f, indent=2)
        
        return filename
    except Exception as e:
        print(f"Error saving working cookies: {e}")
        return None

def check_cookies_interactive(num_to_check=None):
    """Interactive cookie checker"""
    print("Interactive Cookie Checker")
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
    
    # Ask how many to check if not specified
    if num_to_check is None:
        print(f"\nAvailable cookie files:")
        for i, file in enumerate(cookie_files[:10], 1):
            timestamp = datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{i}. {file} - {timestamp}")
        
        try:
            num_to_check = int(input(f"\nHow many cookies to check? (1-{len(cookie_files)}): "))
            if num_to_check < 1 or num_to_check > len(cookie_files):
                num_to_check = min(5, len(cookie_files))
                print(f"Invalid input. Using {num_to_check} cookies.")
        except:
            num_to_check = min(5, len(cookie_files))
            print(f"Invalid input. Using {num_to_check} cookies.")
    
    # Get files to check
    files_to_check = cookie_files[:num_to_check]
    
    print(f"\nChecking {len(files_to_check)} cookie files...")
    
    working_cookies = []
    failed_cookies = []
    all_working_cookie_data = []
    
    for i, file_path in enumerate(files_to_check, 1):
        try:
            print(f"Testing file {i}/{len(files_to_check)}: {file_path}")
            
            # Load cookies from file
            with open(file_path, 'r') as f:
                cookies = json.load(f)
            
            # Test cookies
            is_working, message = test_cookies_advanced(cookies)
            
            file_info = {
                'file': os.path.basename(file_path),
                'cookies_count': len(cookies),
                'timestamp': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                'message': message,
                'cookies_data': cookies
            }
            
            if is_working:
                working_cookies.append(file_info)
                all_working_cookie_data.extend(cookies)
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
    
    # Save working cookies to file
    working_cookies_file = None
    if all_working_cookie_data:
        working_cookies_file = save_working_cookies(all_working_cookie_data)
        print(f"\nSaved {len(all_working_cookie_data)} working cookies to: {working_cookies_file}")
    
    # Prepare response
    response = f"COOKIE CHECK RESULTS - Checked {len(files_to_check)} files\n\n"
    
    if working_cookies:
        response += f"WORKING COOKIES ({len(working_cookies)}):\n"
        for cookie in working_cookies:
            response += f"- {cookie['file']} ({cookie['cookies_count']} cookies) - {cookie['timestamp']}\n"
            response += f"  Status: {cookie['message']}\n\n"
    else:
        response += "NO WORKING COOKIES FOUND\n\n"
    
    if failed_cookies:
        response += f"FAILED COOKIES ({len(failed_cookies)}):\n"
        for cookie in failed_cookies[:3]:  # Show only first 3 failed
            if 'error' in cookie:
                response += f"- {cookie['file']} - Error: {cookie['error']}\n"
            else:
                response += f"- {cookie['file']} - {cookie['message']}\n"
        
        if len(failed_cookies) > 3:
            response += f"... and {len(failed_cookies) - 3} more failed cookies\n"
    
    response += f"\nSUMMARY:\n"
    response += f"- Total checked: {len(files_to_check)}\n"
    response += f"- Working: {len(working_cookies)}\n"
    response += f"- Failed: {len(failed_cookies)}\n"
    
    if working_cookies:
        response += f"\nRECOMMENDATION: Use the most recent working cookie file:\n"
        response += f"{working_cookies[0]['file']}\n"
        response += f"{working_cookies[0]['timestamp']}\n"
        
        if working_cookies_file:
            response += f"\nWORKING COOKIES SAVED TO: {working_cookies_file}\n"
            response += f"This file contains {len(all_working_cookie_data)} working cookies ready for import!"
    else:
        response += f"\nWARNING: No working cookies found. The seller might be offline or cookies have expired.\n"
    
    print("\nSending to Telegram...")
    print(response)
    
    success = send_telegram_message(response)
    
    if success:
        print("Message sent to Telegram successfully!")
        if working_cookies_file:
            print(f"Working cookies saved to: {working_cookies_file}")
    else:
        print("Failed to send message to Telegram")

def main():
    """Main function with command line options"""
    import sys
    
    if len(sys.argv) > 1:
        try:
            num_to_check = int(sys.argv[1])
            check_cookies_interactive(num_to_check)
        except:
            print("Invalid number. Using interactive mode.")
            check_cookies_interactive()
    else:
        check_cookies_interactive()

if __name__ == "__main__":
    main()
