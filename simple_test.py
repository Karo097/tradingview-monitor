#!/usr/bin/env python3
"""
Simple test for TradingView seller status
"""

import requests
import json
import re
import html
from datetime import datetime

def test_seller():
    print("TESTING TRADINGVIEW SELLER STATUS")
    print("=" * 50)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        url = "https://www.oxaam.com/tradecookienew45.php?key=WH87A345N94WDLY"
        print(f"Fetching from: {url}")
        
        response = requests.get(url, timeout=30)
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print(f"Content Length: {len(content)} characters")
            
            # Look for JSON pattern
            json_pattern = r'\[.*?\]'
            matches = re.findall(json_pattern, content, re.DOTALL)
            
            if matches:
                print(f"Found JSON data: {len(matches)} matches")
                
                try:
                    decoded = html.unescape(matches[0])
                    cookies = json.loads(decoded)
                    print(f"Parsed Cookies: {len(cookies)} cookies")
                    
                    # Check critical cookies
                    critical_cookies = ['sessionid', 'sessionid_sign', 'device_t']
                    cookie_values = {c['name']: c['value'] for c in cookies}
                    
                    print("\nCRITICAL COOKIES CHECK:")
                    for critical in critical_cookies:
                        if critical in cookie_values:
                            value = cookie_values[critical]
                            print(f"FOUND {critical}: {value[:20]}..." if len(value) > 20 else f"FOUND {critical}: {value}")
                        else:
                            print(f"MISSING {critical}")
                    
                    present_critical = [c for c in critical_cookies if c in cookie_values]
                    print(f"\nSUMMARY:")
                    print(f"Critical cookies present: {len(present_critical)}/{len(critical_cookies)}")
                    
                    if len(present_critical) >= 2:
                        print("SELLER IS ACTUALLY ONLINE!")
                        print("Fresh cookies are available")
                        
                        # Save cookies
                        with open("fresh_tradingview_cookies.json", "w") as f:
                            json.dump(cookies, f, indent=2)
                        print(f"SAVED {len(cookies)} cookies to fresh_tradingview_cookies.json")
                        
                        return True
                    else:
                        print("SELLER IS OFFLINE - insufficient cookies")
                        return False
                        
                except Exception as e:
                    print(f"Error parsing cookies: {e}")
                    return False
            else:
                print("No JSON data found")
                return False
        else:
            print(f"HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

if __name__ == "__main__":
    is_online = test_seller()
    
    if is_online:
        print("\n" + "="*50)
        print("SUCCESS: You can import fresh_tradingview_cookies.json to your browser!")
    else:
        print("\nSELLER IS OFFLINE - Try again later")
