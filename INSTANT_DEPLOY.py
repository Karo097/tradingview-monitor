#!/usr/bin/env python3
"""
Instant Deployment Script for TradingView Monitor
This script will help you deploy the updated files to GitHub quickly
"""

import os
import webbrowser
import time
import subprocess
import sys

def main():
    print("🚀 TradingView Monitor - Instant Deploy")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("web_monitor.py"):
        print("❌ Error: web_monitor.py not found!")
        print("Please run this script from the tradingview-cookies directory")
        return
    
    print("✅ Files ready for deployment:")
    print("   - web_monitor.py (updated with all fixes)")
    print("   - email_notifier.py (improved email handling)")
    print("   - requirements.txt (dependencies)")
    print("   - Procfile (Render.com config)")
    print()
    
    print("🎯 What's been fixed:")
    print("   ✅ Email address removed from public display")
    print("   ✅ UI shows 30 minutes (not 5 minutes)")
    print("   ✅ 3-hour email notifications (not spam)")
    print("   ✅ Persistent cookie storage for offline access")
    print("   ✅ Download endpoint for saved cookies")
    print()
    
    # Open GitHub repository
    print("🌐 Opening GitHub repository...")
    github_url = "https://github.com/Karo097/tradingview-monitor"
    webbrowser.open(github_url)
    
    print("📋 DEPLOYMENT INSTRUCTIONS:")
    print("=" * 30)
    print("1. GitHub should open in your browser")
    print("2. Click 'Add file' → 'Upload files'")
    print("3. Upload these 2 files:")
    print("   - web_monitor.py")
    print("   - email_notifier.py")
    print("4. Commit message: 'Fix privacy, monitoring, and add cookie storage'")
    print("5. Click 'Commit changes'")
    print()
    
    print("⏰ After upload:")
    print("- Render.com will auto-deploy in 2-3 minutes")
    print("- Check: https://tradingview-monitor.onrender.com")
    print("- Your email will be hidden from public view")
    print("- Monitoring will show 30 minutes")
    print("- Cookies will be saved automatically")
    print()
    
    # Wait for user to complete upload
    input("Press Enter after you've uploaded the files to GitHub...")
    
    print("🎉 Deployment initiated!")
    print("Check your Render.com dashboard for deployment progress")
    print("Your updated service will be live in 2-3 minutes!")
    
    # Open Render.com dashboard
    print("\n🌐 Opening Render.com dashboard...")
    render_url = "https://dashboard.render.com"
    webbrowser.open(render_url)
    
    print("\n✅ All done! Your TradingView monitor is being updated!")

if __name__ == "__main__":
    main()
