#!/usr/bin/env python3
"""
Check Render.com service status and email capabilities
"""
import requests
import json
from datetime import datetime

def check_render_service():
    """Check if Render.com service is running"""
    try:
        print("Checking Render.com service...")
        response = requests.get('https://tradingview-monitor.onrender.com/status', timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Service Response: {data}")
            
            # Check last check time
            last_check = data.get('last_check', '')
            if last_check:
                print(f"Last Check: {last_check}")
                
                # Parse timestamp
                try:
                    last_time = datetime.strptime(last_check, '%Y-%m-%d %H:%M:%S')
                    now = datetime.now()
                    diff = now - last_time
                    
                    print(f"Time since last check: {diff}")
                    
                    if diff.total_seconds() > 3600:  # More than 1 hour
                        print("WARNING: Service hasn't checked in over 1 hour!")
                        print("The monitoring loop might be broken.")
                    else:
                        print("Service is checking regularly.")
                        
                except Exception as e:
                    print(f"Error parsing timestamp: {e}")
            
            return True, data
        else:
            print(f"Service Error: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"Connection Error: {e}")
        return False, None

def check_monitoring_log():
    """Check the monitoring log"""
    try:
        print("\nChecking monitoring log...")
        response = requests.get('https://tradingview-monitor.onrender.com/monitoring-log', timeout=15)
        print(f"Log Status: {response.status_code}")
        
        if response.status_code == 200:
            log_data = response.json()
            print(f"Log Data: {log_data}")
            return True
        else:
            print(f"Log Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Log check error: {e}")
        return False

def test_email_capability():
    """Test if email sending works"""
    try:
        print("\nTesting email capability...")
        
        # Try to access a test endpoint (if it exists)
        test_data = {
            "test": True,
            "message": "Testing email system"
        }
        
        # This would be a test endpoint - let's see if we can trigger an email
        print("Note: Render.com free tier might block outbound SMTP connections")
        print("This could be why emails are not being sent.")
        
        return False
        
    except Exception as e:
        print(f"Email test error: {e}")
        return False

def check_render_limitations():
    """Check Render.com limitations"""
    print("\nRender.com Free Tier Limitations:")
    print("- Outbound SMTP connections are often blocked")
    print("- Email sending might not work on free tier")
    print("- Only inbound HTTP requests are allowed")
    print("- Background processes might sleep after inactivity")

def main():
    print("Render.com Service Diagnostic")
    print("=" * 50)
    print(f"Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check service
    service_ok, service_data = check_render_service()
    log_ok = check_monitoring_log()
    
    # Check limitations
    check_render_limitations()
    
    print("\nDIAGNOSTIC SUMMARY:")
    print(f"Service Status: {'OK' if service_ok else 'FAILED'}")
    print(f"Log Access: {'OK' if log_ok else 'FAILED'}")
    
    if service_ok and service_data:
        last_check = service_data.get('last_check', '')
        if last_check:
            try:
                last_time = datetime.strptime(last_check, '%Y-%m-%d %H:%M:%S')
                now = datetime.now()
                diff = now - last_time
                
                if diff.total_seconds() > 3600:
                    print("\nISSUE IDENTIFIED:")
                    print("- Service is not checking regularly")
                    print("- Monitoring loop might be broken")
                    print("- This could be due to Render.com free tier limitations")
                else:
                    print("\nSERVICE IS WORKING:")
                    print("- Regular checks are happening")
                    print("- Issue might be with email sending")
                    print("- Render.com might block SMTP connections")
                    
            except Exception as e:
                print(f"Error analyzing timestamps: {e}")
    
    print("\nRECOMMENDATIONS:")
    print("1. Check if Render.com free tier supports email sending")
    print("2. Consider using a webhook service for notifications")
    print("3. Use a different email service (SendGrid, Mailgun, etc.)")
    print("4. Check Render.com logs for SMTP errors")

if __name__ == "__main__":
    main()
