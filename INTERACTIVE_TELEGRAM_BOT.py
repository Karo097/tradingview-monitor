#!/usr/bin/env python3
"""
Interactive Telegram Bot that responds to commands
"""

import requests
import json
import os
import glob
from datetime import datetime
import time

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = "7405449740:AAFWd4zQYqr8JyRTPB5jQ0oPV_D00ep28Ms"
TELEGRAM_CHAT_ID = 780489145
TELEGRAM_SEND_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
TELEGRAM_GET_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"

class InteractiveTradingViewBot:
    def __init__(self):
        self.last_update_id = 0
        self.cookie_files = []
        self.load_cookie_files()
    
    def load_cookie_files(self):
        """Load all available cookie files"""
        try:
            # Look in the tradingview-cookies directory
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            pattern = os.path.join(script_dir, "tradingview_cookies*.json")
            self.cookie_files = glob.glob(pattern)
            self.cookie_files.sort(key=os.path.getmtime, reverse=True)
            print(f"Found {len(self.cookie_files)} cookie files in {script_dir}")
        except Exception as e:
            print(f"Error loading cookie files: {e}")
            self.cookie_files = []
    
    def send_message(self, message):
        """Send message to Telegram"""
        try:
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            }
            
            response = requests.post(
                TELEGRAM_SEND_URL,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"Message sent: {message[:50]}...")
                return True
            else:
                print(f"Failed to send message: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def get_updates(self):
        """Get new messages from Telegram"""
        try:
            payload = {
                "offset": self.last_update_id + 1,
                "timeout": 30
            }
            
            response = requests.get(
                TELEGRAM_GET_URL,
                params=payload,
                timeout=35
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and data.get('result'):
                    return data['result']
            return []
            
        except Exception as e:
            print(f"Error getting updates: {e}")
            return []
    
    def test_cookies_advanced(self, cookies):
        """Test if cookies work with TradingView"""
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
                ("https://www.tradingview.com/chart/", "Chart page")
            ]
            
            working_pages = []
            
            for url, description in test_urls:
                try:
                    response = session.get(url, timeout=10)
                    if response.status_code == 200:
                        content = response.text.lower()
                        
                        # Check for signs of successful login
                        login_indicators = [
                            'logout', 'sign out', 'account', 'profile',
                            'premium', 'pro', 'advanced', 'real-time'
                        ]
                        
                        found_indicators = []
                        for indicator in login_indicators:
                            if indicator in content:
                                found_indicators.append(indicator)
                        
                        if found_indicators:
                            working_pages.append(f"{description}: {', '.join(found_indicators[:2])}")
                                
                except Exception as e:
                    continue
            
            if len(working_pages) >= 1:
                return True, f"Working: {working_pages[0]}"
            else:
                return False, "Not working: No login indicators found"
                
        except Exception as e:
            return False, f"Error testing cookies: {e}"
    
    def save_working_cookies(self, working_cookies, filename_prefix="working_cookies"):
        """Save working cookies to a file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{filename_prefix}_{timestamp}.json"
            
            # Save in the same directory as the script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(script_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(working_cookies, f, indent=2)
            
            return filename
        except Exception as e:
            print(f"Error saving working cookies: {e}")
            return None
    
    def check_cookies(self, num_to_check=5):
        """Check cookies and return results"""
        try:
            if not self.cookie_files:
                return "No cookie files found. Run the hourly check first."
            
            # Reload cookie files to get the latest
            self.load_cookie_files()
            
            # Limit to available files
            actual_num = min(num_to_check, len(self.cookie_files))
            files_to_check = self.cookie_files[:actual_num]
            working_cookies = []
            failed_cookies = []
            all_working_cookie_data = []
            
            for i, file_path in enumerate(files_to_check, 1):
                try:
                    print(f"Testing file {i}/{len(files_to_check)}: {file_path}")
                    
                    with open(file_path, 'r') as f:
                        cookies = json.load(f)
                    
                    is_working, message = self.test_cookies_advanced(cookies)
                    
                    file_info = {
                        'file': os.path.basename(file_path),
                        'cookies_count': len(cookies),
                        'timestamp': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                        'message': message
                    }
                    
                    if is_working:
                        working_cookies.append(file_info)
                        all_working_cookie_data.extend(cookies)
                    else:
                        failed_cookies.append(file_info)
                        
                except Exception as e:
                    failed_cookies.append({
                        'file': os.path.basename(file_path),
                        'error': str(e)
                    })
            
            # Save working cookies to file
            working_cookies_file = None
            if all_working_cookie_data:
                working_cookies_file = self.save_working_cookies(all_working_cookie_data)
                print(f"Saved {len(all_working_cookie_data)} working cookies to: {working_cookies_file}")
            
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
                for cookie in failed_cookies[:3]:
                    if 'error' in cookie:
                        response += f"- {cookie['file']} - Error: {cookie['error']}\n"
                    else:
                        response += f"- {cookie['file']} - {cookie['message']}\n"
            
            response += f"\nSUMMARY:\n"
            response += f"- Total checked: {len(files_to_check)}\n"
            response += f"- Working: {len(working_cookies)}\n"
            response += f"- Failed: {len(failed_cookies)}\n"
            
            if working_cookies:
                response += f"\nRECOMMENDATION: Use {working_cookies[0]['file']}\n"
                response += f"Timestamp: {working_cookies[0]['timestamp']}\n"
                
                if working_cookies_file:
                    response += f"\nWORKING COOKIES SAVED TO: {working_cookies_file}\n"
                    response += f"This file contains {len(all_working_cookie_data)} working cookies ready for import!\n"
                    response += f"Download link: https://github.com/Karo097/tradingview-monitor/raw/main/{working_cookies_file}\n"
            else:
                response += f"\nWARNING: No working cookies found. The seller might be offline.\n"
            
            return response
            
        except Exception as e:
            return f"Error checking cookies: {e}"
    
    def handle_command(self, message_text):
        """Handle incoming commands"""
        message_text = message_text.lower().strip()
        
        if message_text in ['/start', 'start', 'hello', 'hi']:
            return """Welcome to TradingView Cookie Bot!

Available commands:
- check cookies
- check 5 cookies
- check 10 cookies
- check all cookies
- help

Just type any of these commands and I'll check your cookies!"""
        
        elif message_text in ['/help', 'help']:
            return """TradingView Cookie Bot Commands:

- check cookies (checks last 5)
- check 5 cookies
- check 10 cookies  
- check all cookies
- list files (show available files)
- help

I'll test your saved cookies and tell you which ones are working!
I'll also create a file with working cookies ready for import."""
        
        elif message_text in ['check cookies', 'check 5 cookies', 'check 5']:
            return self.check_cookies(5)
        
        elif message_text in ['check 10 cookies', 'check 10']:
            return self.check_cookies(10)
        
        elif message_text in ['check all cookies', 'check all']:
            return self.check_cookies(999)
        
        elif message_text in ['list files', 'show files', 'files']:
            if not self.cookie_files:
                return "No cookie files found. Run the hourly check first."
            
            self.load_cookie_files()
            response = f"Available cookie files ({len(self.cookie_files)}):\n\n"
            for i, file_path in enumerate(self.cookie_files[:10], 1):
                filename = os.path.basename(file_path)
                timestamp = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                response += f"{i}. {filename} - {timestamp}\n"
            
            if len(self.cookie_files) > 10:
                response += f"... and {len(self.cookie_files) - 10} more files\n"
            
            response += f"\nUse 'check all cookies' to test all {len(self.cookie_files)} files."
            return response
        
        else:
            return """I didn't understand that command.

Available commands:
- check cookies
- check 5 cookies
- check 10 cookies
- check all cookies
- list files
- help

Type 'help' for more information."""
    
    def run(self):
        """Main bot loop"""
        print("Starting Interactive TradingView Bot...")
        print("Bot is now listening for messages...")
        print("Send 'hello' or 'check cookies' to test!")
        
        # Send startup message
        self.send_message("Bot is now online! Send 'hello' or 'check cookies' to get started.")
        
        while True:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update['update_id']
                    
                    if 'message' in update:
                        message = update['message']
                        chat_id = message['chat']['id']
                        text = message.get('text', '')
                        
                        # Only respond to messages from authorized chat
                        if chat_id == TELEGRAM_CHAT_ID:
                            print(f"Received message: {text}")
                            
                            # Handle the command
                            response = self.handle_command(text)
                            
                            # Send response
                            self.send_message(response)
                
                # Small delay to avoid overwhelming the API
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\nBot stopped by user.")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(5)

def main():
    """Main function"""
    bot = InteractiveTradingViewBot()
    bot.run()

if __name__ == "__main__":
    main()
