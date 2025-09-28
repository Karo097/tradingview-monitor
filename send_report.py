#!/usr/bin/env python3
"""
Send TradingView monitor status report via email
"""

import requests
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_status_report():
    """Get current status from both local and cloud servers"""
    report = []
    report.append("TRADINGVIEW MONITOR STATUS REPORT")
    report.append("=" * 50)
    report.append(f"Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Check local status
    report.append("LOCAL SERVER STATUS:")
    try:
        response = requests.get('http://localhost:5000/status', timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            report.append(f"Online: {status_data.get('online', 'Unknown')}")
            report.append(f"Message: {status_data.get('message', 'No message')}")
            report.append(f"Last Check: {status_data.get('last_check', 'Never')}")
        else:
            report.append(f"Local server error: {response.status_code}")
    except Exception as e:
        report.append(f"Local server not responding: {e}")
    
    report.append("")
    
    # Check cloud status
    report.append("CLOUD SERVER STATUS:")
    try:
        response = requests.get('https://tradingview-monitor.onrender.com/status', timeout=10)
        if response.status_code == 200:
            status_data = response.json()
            report.append(f"Online: {status_data.get('online', 'Unknown')}")
            report.append(f"Message: {status_data.get('message', 'No message')}")
            report.append(f"Last Check: {status_data.get('last_check', 'Never')}")
        else:
            report.append(f"Cloud server error: {response.status_code}")
    except Exception as e:
        report.append(f"Cloud server error: {e}")
    
    report.append("")
    
    # Check monitoring log
    report.append("MONITORING LOG:")
    try:
        response = requests.get('https://tradingview-monitor.onrender.com/monitoring-log', timeout=10)
        if response.status_code == 200:
            log_data = response.json()
            if log_data.get('success'):
                report.append(f"Last Check: {log_data.get('last_check', 'Never')}")
                report.append(f"Cookies Saved: {log_data.get('cookies_saved', 0)}")
                log_content = log_data.get('log', '')
                if log_content:
                    log_lines = log_content.strip().split('\n')
                    report.append(f"Log Entries: {len(log_lines)}")
                    report.append("Recent Entries:")
                    for line in log_lines[-5:]:  # Show last 5 entries
                        if line.strip():
                            report.append(f"   {line}")
                else:
                    report.append("No log entries found")
            else:
                report.append(f"Log error: {log_data.get('message', 'Unknown error')}")
        else:
            report.append(f"Log server error: {response.status_code}")
    except Exception as e:
        report.append(f"Log server error: {e}")
    
    report.append("")
    report.append("SUMMARY:")
    report.append("- Local server: Running for immediate testing")
    report.append("- Cloud server: Running 24/7 monitoring")
    report.append("- Email notifications: Every 3 hours when seller is online")
    report.append("- Cookie storage: Automatic when seller is online")
    
    return "\n".join(report)

def send_email_report():
    """Send status report via email"""
    try:
        # Get status report
        report_content = get_status_report()
        
        # Email configuration
        sender_email = "karo.jihad@gmail.com"
        recipient_email = "karo.jihad@gmail.com"
        password = "mlmo swho bdgp kadg"  # App password
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"TradingView Monitor Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Add body
        msg.attach(MIMEText(report_content, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("SUCCESS: Status report sent to karo.jihad@gmail.com")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to send email - {e}")
        return False

if __name__ == "__main__":
    print("Getting status report...")
    report = get_status_report()
    print(report)
    print("\n" + "="*50)
    print("Sending email report...")
    send_email_report()
