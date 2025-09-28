#!/usr/bin/env python3
"""
TradingView Cookie Manager - Simple and Working
"""

import json
import time
import requests
import re
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TradingViewManager:
    def __init__(self):
        self.cookies_file = "tradingview_cookies.json"
        self.refresh_url = "https://www.oxaam.com/tradecookienew45.php?key=WH87A345N94WDLY"
        self.cookies = []
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        self.load_cookies()
    
    def load_cookies(self):
        try:
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'r') as f:
                    self.cookies = json.load(f)
                logger.info(f"Loaded {len(self.cookies)} cookies")
            else:
                self.cookies = []
        except Exception as e:
            logger.error(f"Error loading cookies: {e}")
            self.cookies = []
    
    def save_cookies(self):
        try:
            with open(self.cookies_file, 'w') as f:
                json.dump(self.cookies, f, indent=2)
            logger.info(f"Saved {len(self.cookies)} cookies")
        except Exception as e:
            logger.error(f"Error saving cookies: {e}")
    
    def fetch_fresh_cookies(self) -> Tuple[bool, List[Dict], str]:
        try:
            logger.info("Fetching fresh cookies...")
            response = self.session.get(self.refresh_url, timeout=30)
            response.raise_for_status()
            
            content = response.text
            cookies = self._extract_cookies_from_response(content)
            
            if cookies:
                # Check if cookies are actually fresh (not the same as current ones)
                current_cookie_values = {c['name']: c['value'] for c in self.cookies}
                new_cookie_values = {c['name']: c['value'] for c in cookies}
                
                # Check if critical cookies have changed
                critical_cookies = ['sessionid', 'sessionid_sign', 'device_t']
                changed_critical = 0
                
                for critical in critical_cookies:
                    if critical in current_cookie_values and critical in new_cookie_values:
                        if current_cookie_values[critical] != new_cookie_values[critical]:
                            changed_critical += 1
                
                if changed_critical == 0:
                    logger.warning("Fresh cookies received but critical cookies haven't changed - original user might be offline")
                    # Still return the cookies but mark as potentially stale
                    return True, cookies, "Fresh cookies received but original user might be offline - cookies may be stale"
                else:
                    logger.info(f"Successfully fetched {len(cookies)} fresh cookies ({changed_critical} critical cookies changed)")
                    return True, cookies, f"Successfully fetched {len(cookies)} fresh cookies ({changed_critical} critical cookies changed)"
            else:
                return False, [], "No valid cookies found in response"
                
        except Exception as e:
            logger.error(f"Error fetching cookies: {e}")
            return False, [], f"Error: {e}"
    
    def _extract_cookies_from_response(self, content: str) -> List[Dict]:
        cookies = []
        try:
            json_pattern = r'\[.*?\]'
            json_matches = re.findall(json_pattern, content, re.DOTALL)
            
            for match in json_matches:
                try:
                    if len(match) < 100:
                        continue
                    
                    import html
                    decoded_match = html.unescape(match)
                    cookie_data = json.loads(decoded_match)
                    
                    if isinstance(cookie_data, list) and len(cookie_data) > 0:
                        all_valid = all(isinstance(item, dict) and 'name' in item and 'value' in item for item in cookie_data)
                        if all_valid:
                            cookies = cookie_data
                            logger.info("Found cookies in JSON format")
                            break
                except json.JSONDecodeError:
                    continue
            
            return cookies
        except Exception as e:
            logger.error(f"Error extracting cookies: {e}")
            return []
    
    def update_cookies(self, new_cookies: List[Dict]):
        existing_cookies = {cookie['name']: cookie for cookie in self.cookies}
        for new_cookie in new_cookies:
            name = new_cookie['name']
            existing_cookies[name] = new_cookie
        self.cookies = list(existing_cookies.values())
        self.save_cookies()
    
    def get_cookie_string(self) -> str:
        cookie_pairs = []
        for cookie in self.cookies:
            if cookie.get('value') and cookie.get('value') != '*':
                cookie_pairs.append(f"{cookie['name']}={cookie['value']}")
        return "; ".join(cookie_pairs)
    
    def test_login(self) -> bool:
        """Test if cookies actually work for login"""
        try:
            # Test with a more realistic browser-like request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cookie': self.get_cookie_string()
            }

            # Test multiple pages to be more accurate
            test_urls = [
                'https://www.tradingview.com/',
                'https://www.tradingview.com/u/',  # User profile page - requires login
                'https://www.tradingview.com/chart/'  # Charts page
            ]

            # Check the last response (charts page) for content analysis
            # Use the response from the last URL tested (charts page)
            response = self.session.get('https://www.tradingview.com/chart/', headers=headers, timeout=10, allow_redirects=True)
            content = response.text.lower()
            final_url = response.url.lower()

            # If redirected to login, definitely failed
            if any(indicator in final_url for indicator in ['login', 'signin', 'auth']):
                logger.warning("Login test FAILED - redirected to login page")
                return False

            # Check if we can access user-specific content that requires login
            # This is a more realistic test - if we can access user data, we're logged in
            user_content_indicators = [
                'user-profile', 'user-settings', 'user-menu', 'profile-dropdown',
                'my-watchlists', 'my-charts', 'user-dashboard', 'account-settings',
                'logged-in', 'authenticated', 'user-logged-in', 'welcome-back'
            ]

            has_user_content = any(indicator in content for indicator in user_content_indicators)

            if has_user_content:
                logger.info("Login test PASSED - found user-specific content")
                return True
            else:
                # If we only see basic content without login indicators, likely not logged in
                logger.warning("Login test FAILED - only basic content found, no login indicators")
                return False

        except Exception as e:
            logger.error(f"Error in login test: {e}")
            return False
    
    def validate_cookies(self) -> Tuple[bool, List[str]]:
        issues = []
        current_time = time.time()
        
        critical_cookies = ['sessionid', 'sessionid_sign', 'device_t']
        cookie_names = {cookie['name'] for cookie in self.cookies}
        
        for critical in critical_cookies:
            if critical not in cookie_names:
                issues.append(f"Missing critical cookie: {critical}")
        
        for cookie in self.cookies:
            if 'expirationDate' in cookie and cookie['expirationDate']:
                exp_time = cookie['expirationDate']
                if exp_time < current_time:
                    issues.append(f"Expired cookie: {cookie['name']} (expired {datetime.fromtimestamp(exp_time)})")
                elif exp_time < current_time + 86400:
                    issues.append(f"Cookie expiring soon: {cookie['name']} (expires {datetime.fromtimestamp(exp_time)})")
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    def refresh_cookies(self) -> bool:
        try:
            success, fresh_cookies, message = self.fetch_fresh_cookies()
            
            if not success:
                logger.error(f"Failed to fetch fresh cookies: {message}")
                return False
            
            self.update_cookies(fresh_cookies)
            
            if self.test_login():
                logger.info("Fresh cookies are working!")
                return True
            else:
                logger.warning("Fresh cookies failed login test")
                return False
                
        except Exception as e:
            logger.error(f"Error refreshing cookies: {e}")
            return False
    
    def get_status(self) -> Dict:
        is_valid, issues = self.validate_cookies()
        login_works = self.test_login()
        
        status = {
            'total_cookies': len(self.cookies),
            'is_valid': is_valid,
            'login_works': login_works,
            'issues': issues,
            'critical_cookies_present': all(
                any(cookie['name'] == name for cookie in self.cookies)
                for name in ['sessionid', 'sessionid_sign', 'device_t']
            )
        }
        
        return status
    
    def print_status(self):
        status = self.get_status()
        
        print("\n" + "="*60)
        print("TRADINGVIEW COOKIE STATUS REPORT")
        print("="*60)
        print(f"Total Cookies: {status['total_cookies']}")
        print(f"Cookie Validity: {'VALID' if status['is_valid'] else 'INVALID'}")
        print(f"Login Test: {'WORKING' if status['login_works'] else 'FAILED'}")
        print(f"Critical Cookies: {'PRESENT' if status['critical_cookies_present'] else 'MISSING'}")
        
        # Show last update time
        if os.path.exists(self.cookies_file):
            mod_time = os.path.getmtime(self.cookies_file)
            last_update = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
            print(f"Last Updated: {last_update}")
        
        if status['issues']:
            print("\nISSUES FOUND:")
            for issue in status['issues']:
                print(f"  • {issue}")
        
        # Add recommendation
        if not status['login_works']:
            print("\n💡 RECOMMENDATION: Use option 4 (Auto-Fix) to refresh cookies")
        elif not status['is_valid']:
            print("\n💡 RECOMMENDATION: Some cookies are expired, consider refreshing")
        else:
            print("\n💡 STATUS: All good! Cookies are working properly")
        
        print("="*60)
    
    def copy_cookies_to_clipboard(self):
        """Copy cookies to clipboard in original JSON format"""
        try:
            import pyperclip
            
            # Create the original JSON array format (multi-line)
            cookies_json = json.dumps(self.cookies, indent=2)
            pyperclip.copy(cookies_json)
            
            print("✅ Cookies copied to clipboard in original JSON format!")
            print("\n📋 MANUAL IMPORT INSTRUCTIONS:")
            print("1. Open your browser extension (Cookie Editor, etc.)")
            print("2. Go to TradingView.com")
            print("3. Open the extension and click 'Import' or 'Add Cookie'")
            print("4. Paste the JSON cookies from clipboard (multi-line format)")
            print("5. Apply/Import the cookies")
            print("6. Refresh the TradingView page")
            print("\n💡 The cookies are now in the same format as your original seller's cookies!")
            return True
        except ImportError:
            print("❌ pyperclip not installed. Installing...")
            try:
                import subprocess
                subprocess.check_call(['py', '-m', 'pip', 'install', 'pyperclip'])
                print("✅ pyperclip installed! Please run this option again.")
                return False
            except Exception as e:
                print(f"❌ Failed to install pyperclip: {e}")
                print("\n📋 MANUAL COPY INSTRUCTIONS:")
                print("Copy this JSON cookie array manually:")
                print(json.dumps(self.cookies, indent=2))
                return False
        except Exception as e:
            print(f"❌ Error copying to clipboard: {e}")
            print("\n📋 MANUAL COPY INSTRUCTIONS:")
            print("Copy this JSON cookie array manually:")
            print(json.dumps(self.cookies, indent=2))
            return False
    
    def auto_fix_cookies(self):
        """Automatically refresh cookies until they work"""
        print("🔧 AUTO-FIXING COOKIES...")
        print("This will keep refreshing until cookies work properly.")

        max_attempts = 5
        stale_count = 0

        for attempt in range(1, max_attempts + 1):
            print(f"\n🔄 Attempt {attempt}/{max_attempts}")

            # Test current cookies first
            print("🔍 Testing current cookies...")
            login_result = self.test_login()

            if login_result:
                print("✅ Current cookies are working!")
                print("🎉 SUCCESS! You can now import these cookies to your browser!")
                return True
            else:
                print("❌ Current cookies not working. Refreshing...")

            # Try to refresh cookies
            success, fresh_cookies, message = self.fetch_fresh_cookies()

            if success:
                print(f"✅ Fresh cookies obtained! ({message})")
                self.update_cookies(fresh_cookies)

                # Check if cookies actually changed
                current_cookies = {c['name']: c['value'] for c in self.cookies}
                critical_cookies = ['sessionid', 'sessionid_sign', 'device_t']

                changed_count = 0
                for cookie_name in critical_cookies:
                    if cookie_name in current_cookies:
                        changed_count += 1

                if changed_count == 0:
                    print("🚫 CRITICAL: Cookies didn't actually change - service returning stale data!")
                    stale_count += 1
                    if stale_count >= 2:
                        print("🚫 STOPPING: Cookies are stale and not updating. Original user offline.")
                        print("💡 The seller's account appears to be offline.")
                        print("⏰ Try again in 30 minutes to 1 hour when the seller is back online.")
                        break
                else:
                    print(f"✅ Cookies updated: {changed_count} critical cookies changed")

                # Test the fresh cookies
                print("🔍 Testing fresh cookies...")
                if self.test_login():
                    print("🎉 SUCCESS! Fresh cookies are working!")
                    print("🎉 You can now import these cookies to your browser!")
                    return True
                else:
                    print("❌ Fresh cookies still not working. Trying again...")
            else:
                print(f"❌ Failed to refresh cookies: {message}")

            if attempt < max_attempts:
                print("⏳ Waiting 5 seconds before next attempt...")
                time.sleep(5)

        print(f"\n❌ Failed to get working cookies after {max_attempts} attempts.")
        print("💡 The original user (seller) appears to be offline or service is returning stale cookies.")
        print("⏰ Try again in 30 minutes to 1 hour when the seller is back online.")
        print("💡 The tool will automatically detect when fresh cookies are available.")

        return False
    
    def create_browser_import_file(self):
        """Create a file with cookies formatted for browser import"""
        try:
            # Create the EXACT same format as original seller's cookies
            filename = "tradingview_cookies_import.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.cookies, f, indent=2)
            
            print(f"✅ Created import file: {filename}")
            print("\n📋 IMPORT INSTRUCTIONS:")
            print("1. Open Firefox with Cookie Editor extension")
            print("2. Go to TradingView.com")
            print("3. Open Cookie Editor extension")
            print("4. Click 'Import' button")
            print(f"5. Select the file: {filename}")
            print("6. Click 'Import' to apply cookies")
            print("7. Refresh TradingView page")
            print("\n💡 This file contains the EXACT same format as your original seller's cookies!")
            
            return filename
            
        except Exception as e:
            print(f"❌ Error creating import file: {e}")
            return None
    
    def show_cookies_format(self):
        """Show cookies in original JSON format"""
        print("\n" + "="*60)
        print("COOKIES IN ORIGINAL JSON FORMAT")
        print("="*60)
        print("This is the exact format that will be copied to clipboard:")
        print("="*60)
        
        cookies_json = json.dumps(self.cookies, indent=2)
        print(cookies_json)
        
        print("="*60)
        print("💡 This matches the format you received from your seller!")
        print("="*60)
    
    def validate_cookies_with_retry(self):
        """Validate cookies and offer retry options"""
        print("🔍 VALIDATING COOKIES WITH RETRY OPTIONS")
        print("="*50)

        max_retries = 3
        for attempt in range(1, max_retries + 1):
            print(f"\n🔄 Validation Attempt {attempt}/{max_retries}")

            # Test login with current cookies
            login_works = self.test_login()

            if login_works:
                print("✅ SUCCESS! Cookies are working!")
                print("🎉 You can now import these cookies to your browser.")
                print("📋 Use option 4 to copy cookies to clipboard")
                return True
            else:
                print("❌ Cookies are NOT working properly.")
                print("🚫 This means the cookies won't work in your browser.")

                if attempt < max_retries:
                    print(f"\n💡 Would you like to try refreshing cookies again? (Attempt {attempt + 1}/{max_retries})")
                    retry = input("Try again? (y/n): ").strip().lower()

                    if retry == 'y' or retry == 'yes':
                        print("🔄 Refreshing cookies...")
                        if self.refresh_cookies():
                            print("✅ Cookies refreshed!")
                            continue
                        else:
                            print("❌ Failed to refresh cookies.")
                    else:
                        print("⏹️  Stopping validation.")
                        break
                else:
                    print("\n❌ FINAL RESULT: Cookies are not working after multiple attempts.")
                    print("🚫 ISSUE: The original cookie seller appears to be offline or the service is returning stale cookies.")
                    print("💡 SOLUTION: Wait and try again later when the seller is back online.")
                    print("⏰ RECOMMENDATION: Try again in 30 minutes to 1 hour.")
                    return False

        return False

    def run_interactive_mode(self):
        while True:
            print("\n" + "="*50)
            print("TRADINGVIEW COOKIE MANAGER")
            print("="*50)
            print("1. Check Status")
            print("2. Test Login")
            print("3. Auto-Fix Cookies (Refresh until working)")
            print("4. Copy Cookies to Clipboard (JSON format)")
            print("5. Create Browser Import File")
            print("6. Show Cookies Format")
            print("7. Validate with Retry Options")
            print("8. Exit")
            print("="*50)

            choice = input("Select an option (1-8): ").strip()

            if choice == '1':
                self.print_status()
            elif choice == '2':
                print("Testing login...")
                if self.test_login():
                    print("✅ Login test successful!")
                else:
                    print("❌ Login test failed")
            elif choice == '3':
                self.auto_fix_cookies()
            elif choice == '4':
                print("Copying cookies to clipboard...")
                self.copy_cookies_to_clipboard()
            elif choice == '5':
                print("Creating browser import file...")
                self.create_browser_import_file()
            elif choice == '6':
                self.show_cookies_format()
            elif choice == '7':
                self.validate_cookies_with_retry()
            elif choice == '8':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

def main():
    print("TradingView Cookie Manager")
    print("=" * 50)
    
    manager = TradingViewManager()
    
    try:
        manager.print_status()
        
        if not manager.test_login():
            print("\n❌ Cookies not working. Auto-fixing...")
            if manager.auto_fix_cookies():
                print("🎉 Cookies are now working!")
            else:
                print("❌ Auto-fix failed. Use option 4 to try again.")
        
        manager.run_interactive_mode()
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()