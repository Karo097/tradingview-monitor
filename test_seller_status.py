#!/usr/bin/env python3
"""
Test if the TradingView seller is actually online by checking fresh cookies
"""

import requests
import json
import re
import html
from datetime import datetime

def test_seller_status():
    """Test if seller is actually online by checking fresh cookies"""
    print("🔍 TESTING TRADINGVIEW SELLER STATUS")
    print("=" * 50)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        url = "https://www.oxaam.com/tradecookienew45.php?key=WH87A345N94WDLY"
        print(f"🌐 Fetching from: {url}")
        
        response = requests.get(url, timeout=30)
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print(f"📄 Content Length: {len(content)} characters")
            
            # Look for JSON pattern
            json_pattern = r'\[.*?\]'
            matches = re.findall(json_pattern, content, re.DOTALL)
            
            if matches:
                print(f"✅ Found JSON data: {len(matches)} matches")
                
                try:
                    decoded = html.unescape(matches[0])
                    cookies = json.loads(decoded)
                    print(f"🍪 Parsed Cookies: {len(cookies)} cookies")
                    
                    # Check critical cookies
                    critical_cookies = ['sessionid', 'sessionid_sign', 'device_t']
                    cookie_values = {c['name']: c['value'] for c in cookies}
                    
                    print("\n🔑 CRITICAL COOKIES CHECK:")
                    for critical in critical_cookies:
                        if critical in cookie_values:
                            value = cookie_values[critical]
                            print(f"✅ {critical}: {value[:20]}..." if len(value) > 20 else f"✅ {critical}: {value}")
                        else:
                            print(f"❌ {critical}: MISSING")
                    
                    present_critical = [c for c in critical_cookies if c in cookie_values]
                    print(f"\n📊 SUMMARY:")
                    print(f"Critical cookies present: {len(present_critical)}/{len(critical_cookies)}")
                    
                    if len(present_critical) >= 2:
                        print("🎉 SELLER IS ACTUALLY ONLINE!")
                        print("✅ Fresh cookies are available")
                        print("✅ You can import these cookies to your browser")
                        
                        # Show session info
                        if 'sessionid' in cookie_values:
                            sessionid = cookie_values['sessionid']
                            print(f"🔐 Session ID: {sessionid}")
                            print(f"📅 Session appears to be active")
                        
                        return True, f"Seller is ONLINE! {len(present_critical)} critical cookies present"
                    else:
                        print("❌ SELLER IS OFFLINE")
                        print("❌ Insufficient critical cookies")
                        return False, "Seller is OFFLINE - insufficient cookies"
                        
                except Exception as e:
                    print(f"❌ Error parsing cookies: {e}")
                    return False, f"Error parsing cookies: {e}"
            else:
                print("❌ No JSON data found in response")
                return False, "No cookies found in response"
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False, f"Service error: HTTP {response.status_code}"
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False, f"Connection error: {e}"

def save_cookies_for_import():
    """Save the fresh cookies for browser import"""
    try:
        url = "https://www.oxaam.com/tradecookienew45.php?key=WH87A345N94WDLY"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            content = response.text
            json_pattern = r'\[.*?\]'
            matches = re.findall(json_pattern, content, re.DOTALL)
            
            if matches:
                decoded = html.unescape(matches[0])
                cookies = json.loads(decoded)
                
                # Save for browser import
                with open("fresh_tradingview_cookies.json", "w") as f:
                    json.dump(cookies, f, indent=2)
                
                print(f"\n💾 SAVED {len(cookies)} FRESH COOKIES")
                print("📁 File: fresh_tradingview_cookies.json")
                print("🌐 Ready for browser import!")
                return True
    except Exception as e:
        print(f"❌ Failed to save cookies: {e}")
        return False

if __name__ == "__main__":
    is_online, message = test_seller_status()
    
    if is_online:
        print("\n" + "="*50)
        print("🎯 SELLER IS ONLINE - SAVING FRESH COOKIES")
        save_cookies_for_import()
        print("\n✅ You can now import fresh_tradingview_cookies.json to your browser!")
    else:
        print(f"\n❌ SELLER IS OFFLINE: {message}")
        print("⏰ Try again later when the seller comes online")
