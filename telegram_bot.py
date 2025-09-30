#!/usr/bin/env python3
"""
Telegram Bot for TradingView Cookie Management
Handles commands to check last 24 cookies and find working ones
"""

import requests
import json
import os
import glob
from datetime import datetime, timedelta
from email_notifier import EmailNotifier

class TradingViewTelegramBot:
    def __init__(self):
        self.notifier = EmailNotifier()
        self.cookie_files = []
        self.load_cookie_files()
    
    def load_cookie_files(self):
        """Load all available cookie files"""
        try:
            # Look for cookie files in current directory
            pattern = "tradingview_cookies*.json"
            self.cookie_files = glob.glob(pattern)
            self.cookie_files.sort(key=os.path.getmtime, reverse=True)
            print(f"Found {len(self.cookie_files)} cookie files")
        except Exception as e:
            print(f"Error loading cookie files: {e}")
            self.cookie_files = []
    
    def test_cookies(self, cookies):
        """Test if cookies are working by checking TradingView login"""
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
            
            # Test login by accessing TradingView
            test_urls = [
                "https://www.tradingview.com/",
                "https://www.tradingview.com/chart/",
                "https://www.tradingview.com/accounts/"
            ]
            
            for url in test_urls:
                try:
                    response = session.get(url, timeout=10)
                    if response.status_code == 200:
                        content = response.text.lower()
                        
                        # Check for signs of successful login
                        login_indicators = [
                            'logout', 'sign out', 'account', 'profile',
                            'premium', 'pro', 'advanced', 'real-time'
                        ]
                        
                        for indicator in login_indicators:
                            if indicator in content:
                                return True, f"Login successful - found '{indicator}' on {url}"
                        
                        # Check for login page indicators (means not logged in)
                        if 'sign in' in content or 'login' in content:
                            continue
                            
                except Exception as e:
                    print(f"Error testing {url}: {e}")
                    continue
            
            return False, "No login indicators found"
            
        except Exception as e:
            return False, f"Error testing cookies: {e}"
    
    def check_last_24_cookies(self):
        """Check the last 24 cookie files to find working ones"""
        try:
            print("Checking last 24 cookie files...")
            
            # Get last 24 files (or all available if less than 24)
            files_to_check = self.cookie_files[:24]
            
            if not files_to_check:
                return "No cookie files found. Run the hourly check first to generate some cookies."
            
            working_cookies = []
            failed_cookies = []
            
            for i, file_path in enumerate(files_to_check, 1):
                try:
                    print(f"Checking file {i}/{len(files_to_check)}: {file_path}")
                    
                    # Load cookies from file
                    with open(file_path, 'r') as f:
                        cookies = json.load(f)
                    
                    # Test cookies
                    is_working, message = self.test_cookies(cookies)
                    
                    file_info = {
                        'file': file_path,
                        'cookies_count': len(cookies),
                        'timestamp': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                        'message': message
                    }
                    
                    if is_working:
                        working_cookies.append(file_info)
                        print(f"✅ WORKING: {file_path}")
                    else:
                        failed_cookies.append(file_info)
                        print(f"❌ FAILED: {file_path}")
                        
                except Exception as e:
                    print(f"Error checking {file_path}: {e}")
                    failed_cookies.append({
                        'file': file_path,
                        'error': str(e)
                    })
            
            # Prepare response
            response = f"🔍 COOKIE CHECK RESULTS - Last {len(files_to_check)} files\n\n"
            
            if working_cookies:
                response += f"✅ WORKING COOKIES ({len(working_cookies)}):\n"
                for cookie in working_cookies:
                    response += f"• {cookie['file']} ({cookie['cookies_count']} cookies) - {cookie['timestamp']}\n"
                    response += f"  Status: {cookie['message']}\n\n"
            else:
                response += "❌ NO WORKING COOKIES FOUND\n\n"
            
            if failed_cookies:
                response += f"❌ FAILED COOKIES ({len(failed_cookies)}):\n"
                for cookie in failed_cookies[:5]:  # Show only first 5 failed
                    if 'error' in cookie:
                        response += f"• {cookie['file']} - Error: {cookie['error']}\n"
                    else:
                        response += f"• {cookie['file']} - {cookie['message']}\n"
                
                if len(failed_cookies) > 5:
                    response += f"... and {len(failed_cookies) - 5} more failed cookies\n"
            
            response += f"\n📊 SUMMARY:\n"
            response += f"• Total checked: {len(files_to_check)}\n"
            response += f"• Working: {len(working_cookies)}\n"
            response += f"• Failed: {len(failed_cookies)}\n"
            
            if working_cookies:
                response += f"\n🎯 RECOMMENDATION: Use the most recent working cookie file:\n"
                response += f"📁 {working_cookies[0]['file']}\n"
                response += f"⏰ {working_cookies[0]['timestamp']}\n"
            else:
                response += f"\n⚠️ WARNING: No working cookies found. The seller might be offline or cookies have expired.\n"
                response += f"Try running the hourly check again or wait for the seller to come back online.\n"
            
            return response
            
        except Exception as e:
            return f"Error checking cookies: {e}"
    
    def send_telegram_message(self, message):
        """Send message via Telegram"""
        try:
            return self.notifier.send_notification("Cookie Check Results", message)
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return False
    
    def handle_command(self, command):
        """Handle Telegram commands"""
        command = command.lower().strip()
        
        if command in ['/check', '/check_cookies', 'check cookies', 'check last 24']:
            print("Processing /check command...")
            result = self.check_last_24_cookies()
            return self.send_telegram_message(result)
        
        elif command in ['/help', '/start']:
            help_message = """🤖 TradingView Cookie Bot Commands:

/check - Check last 24 cookie files for working ones
/help - Show this help message

Just send 'check cookies' or 'check last 24' to test your saved cookies!"""
            return self.send_telegram_message(help_message)
        
        else:
            return False

def main():
    """Main function for testing"""
    print("=" * 50)
    print("TradingView Telegram Bot - Cookie Checker")
    print("=" * 50)
    
    bot = TradingViewTelegramBot()
    
    # Test the check command
    print("Testing cookie check...")
    result = bot.check_last_24_cookies()
    print("\n" + "=" * 50)
    print("RESULT:")
    print("=" * 50)
    print(result)
    
    # Send to Telegram
    print("\nSending to Telegram...")
    success = bot.send_telegram_message(result)
    
    if success:
        print("✅ Message sent to Telegram successfully!")
    else:
        print("❌ Failed to send message to Telegram")

if __name__ == "__main__":
    main()
