#!/usr/bin/env python3
"""
Quick status check for TradingView monitor
"""

import requests
import json
from datetime import datetime

def check_status():
    print("🔍 TRADINGVIEW MONITOR STATUS REPORT")
    print("=" * 50)
    print(f"Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check local status
    print("📱 LOCAL SERVER STATUS:")
    try:
        response = requests.get('http://localhost:5000/status', timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Online: {status_data.get('online', 'Unknown')}")
            print(f"📝 Message: {status_data.get('message', 'No message')}")
            print(f"🕐 Last Check: {status_data.get('last_check', 'Never')}")
        else:
            print(f"❌ Local server error: {response.status_code}")
    except Exception as e:
        print(f"❌ Local server not responding: {e}")
    
    print()
    
    # Check cloud status
    print("☁️ CLOUD SERVER STATUS:")
    try:
        response = requests.get('https://tradingview-monitor.onrender.com/status', timeout=10)
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Online: {status_data.get('online', 'Unknown')}")
            print(f"📝 Message: {status_data.get('message', 'No message')}")
            print(f"🕐 Last Check: {status_data.get('last_check', 'Never')}")
        else:
            print(f"❌ Cloud server error: {response.status_code}")
    except Exception as e:
        print(f"❌ Cloud server error: {e}")
    
    print()
    
    # Check monitoring log
    print("📋 MONITORING LOG:")
    try:
        response = requests.get('https://tradingview-monitor.onrender.com/monitoring-log', timeout=10)
        if response.status_code == 200:
            log_data = response.json()
            if log_data.get('success'):
                print(f"✅ Last Check: {log_data.get('last_check', 'Never')}")
                print(f"🍪 Cookies Saved: {log_data.get('cookies_saved', 0)}")
                log_content = log_data.get('log', '')
                if log_content:
                    log_lines = log_content.strip().split('\n')
                    print(f"📊 Log Entries: {len(log_lines)}")
                    print("📝 Recent Entries:")
                    for line in log_lines[-5:]:  # Show last 5 entries
                        if line.strip():
                            print(f"   {line}")
                else:
                    print("📝 No log entries found")
            else:
                print(f"❌ Log error: {log_data.get('message', 'Unknown error')}")
        else:
            print(f"❌ Log server error: {response.status_code}")
    except Exception as e:
        print(f"❌ Log server error: {e}")
    
    print()
    print("🎯 SUMMARY:")
    print("- Local server: Running for immediate testing")
    print("- Cloud server: Running 24/7 monitoring")
    print("- Email notifications: Every 3 hours when seller is online")
    print("- Cookie storage: Automatic when seller is online")

if __name__ == "__main__":
    check_status()
