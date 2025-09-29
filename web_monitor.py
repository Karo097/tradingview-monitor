#!/usr/bin/env python3
"""
TradingView Web Monitor for Render.com (Free Tier)
"""

from flask import Flask, render_template_string, jsonify
import json
import requests
import re
import html
import time
import os
from datetime import datetime, timedelta
import threading
from email_notifier import EmailNotifier

app = Flask(__name__)

class WebMonitor:
    def __init__(self):
        self.email_notifier = EmailNotifier("karo.jihad@gmail.com")
        self.last_check = None
        self.last_status = None
        self.monitoring = False
        self.last_cookies = None
        self.last_email_sent = None
        self.cookie_file = "tradingview_cookies_cloud.json"
        self.start_monitoring()
    
    def send_email_notification(self, subject, message):
        """Send email notification using webhook service"""
        return self.email_notifier.send_notification(subject, message)
    
    def check_seller_status(self):
        """Check if seller is online"""
        try:
            url = "https://www.oxaam.com/tradecookienew45.php?key=WH87A345N94WDLY"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                content = response.text
                json_pattern = r'\[.*?\]'
                matches = re.findall(json_pattern, content, re.DOTALL)
                
                if matches:
                    try:
                        decoded = html.unescape(matches[0])
                        cookies = json.loads(decoded)
                        
                        # Check if critical cookies have changed
                        critical_cookies = ['sessionid', 'sessionid_sign', 'device_t']
                        cookie_values = {c['name']: c['value'] for c in cookies}
                        
                        # Simple check - if we have critical cookies, seller is online
                        present_critical = [c for c in critical_cookies if c in cookie_values]
                        
                        if len(present_critical) >= 2:
                            # Store cookies for offline access
                            self.save_cookies(cookies)
                            return True, f"Seller is ONLINE! {len(present_critical)} critical cookies present"
                        else:
                            return False, "Seller is OFFLINE - insufficient cookies"
                            
                    except Exception as e:
                        return False, f"Error parsing cookies: {e}"
                else:
                    return False, "No cookies found in response"
            else:
                return False, f"Service error: HTTP {response.status_code}"
                
        except Exception as e:
            return False, f"Connection error: {e}"
    
    def save_cookies(self, cookies):
        """Save cookies to file for offline access"""
        try:
            # Save main cookie file
            with open(self.cookie_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            
            # Also create browser import file
            import_file = "tradingview_cookies_browser_import.json"
            with open(import_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            
            self.last_cookies = cookies
            print(f"Saved {len(cookies)} cookies to {self.cookie_file}")
            print(f"Created browser import file: {import_file}")
            
            # Log the cookie save event
            self.log_event(f"COOKIES SAVED: {len(cookies)} cookies saved at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Failed to save cookies: {e}")
            self.log_event(f"ERROR: Failed to save cookies - {e}")
    
    def load_cookies(self):
        """Load saved cookies from file"""
        try:
            with open(self.cookie_file, 'r') as f:
                cookies = json.load(f)
            self.last_cookies = cookies
            print(f"Loaded {len(cookies)} cookies from {self.cookie_file}")
            return cookies
        except Exception as e:
            print(f"Failed to load cookies: {e}")
            return None
    
    
    def log_event(self, message):
        """Log events to file"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open("monitoring_log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            print(f"Failed to log event: {e}")
    
    def monitor_loop(self):
        """Background monitoring loop - only checks at 42 minutes past each hour"""
        while self.monitoring:
            try:
                now = datetime.now()
                current_minute = now.minute
                
                # Only check if it's 42 minutes past the hour
                if current_minute == 42:
                    print(f"[{now.strftime('%H:%M:%S')}] Hourly check time - checking seller status...")
                    
                    is_online, message = self.check_seller_status()
                    self.last_check = now
                    self.last_status = {"online": is_online, "message": message}
                    
                    print(f"[{self.last_check.strftime('%H:%M:%S')}] {message}")
                    self.log_event(f"STATUS CHECK: {message}")
                    
                    if is_online:
                        print("SELLER IS ONLINE!")
                        
                        # Send hourly email notification
                        subject = f"TradingView Hourly Report - {self.last_check.strftime('%H:%M')}"
                        
                        # Get fresh cookies for the email
                        fresh_cookies_json = ""
                        try:
                            if self.last_cookies:
                                fresh_cookies_json = json.dumps(self.last_cookies, indent=2)
                        except:
                            fresh_cookies_json = "Error formatting cookies"
                        
                        email_message = f"""
TradingView Hourly Status Report

Time: {self.last_check.strftime('%Y-%m-%d %H:%M:%S')}
Status: {message}
Cookies Saved: {len(self.last_cookies) if self.last_cookies else 0} cookies

SELLER STATUS: ONLINE
Fresh cookies are available and automatically saved!

FRESH COOKIES (JSON FORMAT):
{fresh_cookies_json}

You can:
1. Copy the JSON above and import to your browser
2. Download fresh cookies: https://tradingview-monitor.onrender.com/download-browser-import
3. Access premium TradingView features

This is your hourly update (sent at 42 minutes past each hour).
Next update: {(self.last_check + timedelta(hours=1)).strftime('%H:%M')}
"""
                        
                        if self.send_email_notification(subject, email_message):
                            print("Hourly email notification sent!")
                            self.last_email_sent = datetime.now()
                        else:
                            print("Failed to send email notification")
                    else:
                        print("Seller is offline.")
                        
                        # Send hourly email even when seller is offline
                        subject = f"TradingView Hourly Report - {self.last_check.strftime('%H:%M')} (OFFLINE)"
                        
                        # Get last saved cookies for the email
                        last_cookies_json = ""
                        try:
                            if self.last_cookies:
                                last_cookies_json = json.dumps(self.last_cookies, indent=2)
                        except:
                            last_cookies_json = "No cookies available"
                        
                        email_message = f"""
TradingView Hourly Status Report

Time: {self.last_check.strftime('%Y-%m-%d %H:%M:%S')}
Status: {message}

SELLER STATUS: OFFLINE
No fresh cookies available at this time.

LAST SAVED COOKIES (JSON FORMAT):
{last_cookies_json}

Download last saved: https://tradingview-monitor.onrender.com/download-browser-import

The system continues monitoring and will notify you when the seller comes back online.

This is your hourly update (sent at 42 minutes past each hour).
Next update: {(self.last_check + timedelta(hours=1)).strftime('%H:%M')}
"""
                        
                        if self.send_email_notification(subject, email_message):
                            print("Hourly offline email notification sent!")
                            self.last_email_sent = datetime.now()
                        else:
                            print("Failed to send email notification")
                    
                    # Wait until next hour to avoid multiple checks in the same minute
                    next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                    wait_seconds = (next_hour - now).total_seconds()
                    print(f"Waiting {wait_seconds/60:.1f} minutes until next check...")
                    time.sleep(wait_seconds)
                else:
                    # Calculate seconds until next 42-minute mark
                    if current_minute < 42:
                        next_42 = now.replace(minute=42, second=0, microsecond=0)
                    else:
                        next_42 = now.replace(hour=now.hour + 1, minute=42, second=0, microsecond=0)
                    
                    wait_seconds = (next_42 - now).total_seconds()
                    print(f"[{now.strftime('%H:%M:%S')}] Waiting {wait_seconds/60:.1f} minutes until next check at {next_42.strftime('%H:%M')}...")
                    time.sleep(wait_seconds)
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                self.log_event(f"ERROR: Monitoring loop error - {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def start_monitoring(self):
        """Start background monitoring"""
        if not self.monitoring:
            self.monitoring = True
            monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            monitor_thread.start()
            print("Monitoring started!")

# Global monitor instance
monitor = WebMonitor()

@app.route('/')
def index():
    """Main page"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TradingView Monitor</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 40px; 
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .status { 
                padding: 20px; 
                border-radius: 5px; 
                margin: 20px 0; 
                font-size: 18px;
            }
            .online { 
                background-color: #d4edda; 
                border: 1px solid #c3e6cb; 
                color: #155724;
            }
            .offline { 
                background-color: #f8d7da; 
                border: 1px solid #f5c6cb; 
                color: #721c24;
            }
            .info {
                background-color: #d1ecf1;
                border: 1px solid #bee5eb;
                color: #0c5460;
            }
            h1 { color: #333; text-align: center; }
            .refresh-btn {
                background: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            .refresh-btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>TradingView Cookie Monitor</h1>
            
            <div id="status" class="status info">
                <h3>Status: Checking...</h3>
                <p>Last check: <span id="lastCheck">Never</span></p>
                <p>Message: <span id="message">Initializing...</span></p>
            </div>
            
             <div class="info">
                 <h3>Notifications</h3>
                 <p>Hourly email reports are sent at 42 minutes past each hour (00:42, 01:42, 02:42, etc.) - 24 emails per day!</p>
             </div>
             
             <div class="info">
                 <h3>How It Works</h3>
                 <p>This monitor checks the TradingView seller only at 42 minutes past each hour and sends hourly email reports with fresh cookies.</p>
             </div>
            
            <button class="refresh-btn" onclick="updateStatus()">Refresh Status</button>
        </div>
        
        <script>
            function updateStatus() {
                fetch('/status')
                    .then(response => response.json())
                    .then(data => {
                        const statusDiv = document.getElementById('status');
                        const lastCheckSpan = document.getElementById('lastCheck');
                        const messageSpan = document.getElementById('message');
                        
                        if (data.online) {
                            statusDiv.className = 'status online';
                            statusDiv.innerHTML = '<h3>Status: SELLER IS ONLINE!</h3><p>Fresh cookies are available!</p>';
                        } else {
                            statusDiv.className = 'status offline';
                            statusDiv.innerHTML = '<h3>Status: Seller is offline</h3><p>Waiting for seller to come online...</p>';
                        }
                        
                        lastCheckSpan.textContent = data.last_check || 'Never';
                        messageSpan.textContent = data.message || 'No data';
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('status').innerHTML = '<h3>Error loading status</h3>';
                    });
            }
            
            // Update status every 30 seconds
            updateStatus();
            setInterval(updateStatus, 30000);
        </script>
    </body>
    </html>
    """
    return html_template

@app.route('/status')
def status():
    """API endpoint for status"""
    if monitor.last_status:
        return jsonify({
            'online': monitor.last_status['online'],
            'message': monitor.last_status['message'],
            'last_check': monitor.last_check.strftime('%Y-%m-%d %H:%M:%S') if monitor.last_check else None
        })
    else:
        # If no status yet, do a quick check
        try:
            is_online, message = monitor.check_seller_status()
            monitor.last_check = datetime.now()
            monitor.last_status = {"online": is_online, "message": message}
            
            return jsonify({
                'online': is_online,
                'message': message,
                'last_check': monitor.last_check.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            return jsonify({
                'online': False,
                'message': f'Error checking status: {e}',
                'last_check': None
            })

@app.route('/check')
def manual_check():
    """Manual check endpoint"""
    is_online, message = monitor.check_seller_status()
    monitor.last_check = datetime.now()
    monitor.last_status = {"online": is_online, "message": message}
    
    return jsonify({
        'online': is_online,
        'message': message,
        'timestamp': monitor.last_check.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/download-cookies')
def download_cookies():
    """Download saved cookies for offline access"""
    try:
        cookies = monitor.load_cookies()
        if cookies:
            return jsonify({
                'success': True,
                'cookies': cookies,
                'count': len(cookies),
                'message': 'Cookies downloaded successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No saved cookies available'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading cookies: {e}'
        })

@app.route('/download-browser-import')
def download_browser_import():
    """Download cookies in browser import format"""
    try:
        import_file = "tradingview_cookies_browser_import.json"
        if os.path.exists(import_file):
            with open(import_file, 'r') as f:
                cookies = json.load(f)
            
            from flask import Response
            return Response(
                json.dumps(cookies, indent=2),
                mimetype='application/json',
                headers={
                    'Content-Disposition': 'attachment; filename=tradingview_cookies_import.json'
                }
            )
        else:
            return jsonify({
                'success': False,
                'message': 'No browser import file available'
            })
    except Exception as e:
         return jsonify({
             'success': False,
             'message': f'Error loading browser import file: {e}'
         })

@app.route('/monitoring-log')
def monitoring_log():
    """Get the monitoring log"""
    try:
        if os.path.exists("monitoring_log.txt"):
            with open("monitoring_log.txt", 'r', encoding="utf-8") as f:
                log_content = f.read()
            
            return jsonify({
                'success': True,
                'log': log_content,
                'last_check': monitor.last_check.strftime('%Y-%m-%d %H:%M:%S') if monitor.last_check else None,
                'last_status': monitor.last_status,
                'cookies_saved': len(monitor.last_cookies) if monitor.last_cookies else 0
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No monitoring log found'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error reading monitoring log: {e}'
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
