#!/usr/bin/env python3
"""
AUTO DEPLOY - TradingView Monitor
This script will automatically deploy your files to GitHub
"""

import os
import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    print("🚀 AUTO DEPLOY - TradingView Monitor")
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
    
    # Initialize git if not already done
    if not os.path.exists(".git"):
        print("🔄 Initializing Git repository...")
        run_command("git init", "Git init")
        run_command("git remote add origin https://github.com/Karo097/tradingview-monitor.git", "Add remote origin")
    
    # Add all files
    run_command("git add .", "Add files to Git")
    
    # Commit changes
    run_command('git commit -m "Fix privacy, monitoring interval, and add cookie storage"', "Commit changes")
    
    # Push to GitHub
    print("🚀 Pushing to GitHub...")
    success = run_command("git push -u origin main", "Push to GitHub")
    
    if success:
        print()
        print("🎉 DEPLOYMENT SUCCESSFUL!")
        print("=" * 30)
        print("✅ Files uploaded to GitHub")
        print("✅ Render.com will auto-deploy in 2-3 minutes")
        print("✅ Check: https://tradingview-monitor.onrender.com")
        print()
        print("🎯 What's been fixed:")
        print("   - Email address removed from public display")
        print("   - UI shows 30 minutes (not 5 minutes)")
        print("   - 3-hour email notifications (not spam)")
        print("   - Persistent cookie storage added")
        print("   - Download endpoint for saved cookies")
    else:
        print()
        print("❌ DEPLOYMENT FAILED!")
        print("Please check your GitHub credentials or try manual upload")
        print("Manual upload: https://github.com/Karo097/tradingview-monitor")

if __name__ == "__main__":
    main()
