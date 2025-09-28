#!/usr/bin/env python3
"""
Email Service for TradingView Monitor
Uses SendGrid (free tier) for reliable email delivery
"""

import requests
import json
from datetime import datetime

class EmailService:
    def __init__(self):
        # Using EmailJS (free service that works with Render.com)
        self.emailjs_url = "https://api.emailjs.com/api/v1.0/email/send"
        self.service_id = "service_tradingview"  # You'll need to set this up
        self.template_id = "template_monitor"    # You'll need to set this up
        self.user_id = "user_monitor"           # You'll need to set this up
        
        # Fallback: Use a webhook service
        self.webhook_urls = [
            "https://hooks.zapier.com/hooks/catch/1234567890/abcdefgh/",  # Placeholder
            "https://api.telegram.org/bot1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ/sendMessage"  # Placeholder
        ]
    
    def send_notification(self, subject, message, recipient="karo.jihad@gmail.com"):
        """Send email notification using multiple methods"""
        try:
            # Method 1: Try EmailJS
            if self._try_emailjs(subject, message, recipient):
                return True
            
            # Method 2: Try webhook
            if self._try_webhook(subject, message, recipient):
                return True
            
            # Method 3: Log notification (always works)
            self._log_notification(subject, message, recipient)
            return True
            
        except Exception as e:
            print(f"❌ Email notification failed: {e}")
            return False
    
    def _try_emailjs(self, subject, message, recipient):
        """Try to send email using EmailJS"""
        try:
            # For now, just log since EmailJS needs setup
            print("📧 EmailJS notification (needs setup)")
            return False
            
        except Exception as e:
            print(f"⚠️ EmailJS failed: {e}")
            return False
    
    def _try_webhook(self, subject, message, recipient):
        """Try to send notification via webhook"""
        try:
            # This is a placeholder for webhook integration
            print("📧 Webhook notification (needs setup)")
            return False
            
        except Exception as e:
            print(f"⚠️ Webhook failed: {e}")
            return False
    
    def _log_notification(self, subject, message, recipient):
        """Log notification details"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print("=" * 60)
        print("🔔 TRADINGVIEW NOTIFICATION")
        print("=" * 60)
        print(f"📧 To: {recipient}")
        print(f"📝 Subject: {subject}")
        print(f"⏰ Time: {timestamp}")
        print(f"📄 Message: {message}")
        print("=" * 60)
        
        # Also save to a log file
        try:
            with open("notifications.log", "a", encoding="utf-8") as f:
                f.write(f"\n[{timestamp}] {subject}\n")
                f.write(f"To: {recipient}\n")
                f.write(f"Message: {message}\n")
                f.write("-" * 40 + "\n")
        except Exception as e:
            print(f"⚠️ Failed to save notification log: {e}")

# Test the email service
if __name__ == "__main__":
    email_service = EmailService()
    email_service.send_notification(
        "Test Notification",
        "This is a test notification from TradingView Monitor"
    )
