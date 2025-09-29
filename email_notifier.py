#!/usr/bin/env python3
"""
Alternative email notification system for Render.com
Uses webhook services since SMTP is blocked
"""

import requests
import json
from datetime import datetime

class EmailNotifier:
    def __init__(self, recipient_email="karo.jihad@gmail.com"):
        self.recipient_email = recipient_email
        # Telegram bot configuration (replace with your bot token and chat ID)
        self.telegram_bot_token = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
        self.telegram_chat_id = "YOUR_CHAT_ID_HERE"  # Get from /getUpdates
        self.telegram_url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
    
    def send_notification(self, subject, message):
        """Send notification using Telegram bot or fallback to logging"""
        try:
            # Try Telegram bot first (works with Render.com free tier)
            if self._try_telegram(subject, message):
                return True
            
            # Fallback to logging
            self._log_notification(subject, message)
            return True
            
        except Exception as e:
            print(f"Notification failed: {e}")
            return False
    
    def _try_telegram(self, subject, message):
        """Try to send notification via Telegram bot"""
        try:
            # Check if Telegram bot is configured
            if (self.telegram_bot_token == "YOUR_BOT_TOKEN_HERE" or 
                self.telegram_chat_id == "YOUR_CHAT_ID_HERE"):
                print("Telegram bot not configured. Please set up bot token and chat ID.")
                return False
            
            # Prepare Telegram message
            telegram_message = f"*{subject}*\n\n{message}"
            
            # Send to Telegram
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": telegram_message,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(
                self.telegram_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"Telegram notification sent: {subject}")
                return True
            else:
                print(f"Telegram failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Telegram notification failed: {e}")
            return False
    
    def _log_notification(self, subject, message):
        """Log notification details"""
        print("=" * 50)
        print("🔔 TRADINGVIEW NOTIFICATION")
        print("=" * 50)
        print(f"📧 To: {self.recipient_email}")
        print(f"📝 Subject: {subject}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📄 Message: {message}")
        print("=" * 50)
    

# Example usage
if __name__ == "__main__":
    notifier = EmailNotifier()
    notifier.send_notification(
        "Test Notification",
        "This is a test notification from TradingView Monitor"
    )
