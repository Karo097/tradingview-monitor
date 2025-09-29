#!/usr/bin/env python3
"""
Simple Web Service for TradingView Hourly Check
Can be hosted on any free web service (PythonAnywhere, Heroku, etc.)
"""

from flask import Flask, jsonify
import subprocess
import sys
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """Home page"""
    return """
    <h1>TradingView Hourly Checker</h1>
    <p>This service checks TradingView seller status and sends Telegram notifications.</p>
    <p>Last check: <span id="lastCheck">Never</span></p>
    <p><a href="/check">Manual Check</a></p>
    <p><a href="/status">Status</a></p>
    
    <script>
        function updateStatus() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('lastCheck').textContent = data.last_check || 'Never';
                });
        }
        updateStatus();
        setInterval(updateStatus, 30000);
    </script>
    """

@app.route('/check')
def manual_check():
    """Manual check endpoint"""
    try:
        # Run the hourly check script
        result = subprocess.run([sys.executable, 'tradingview_hourly_check.py'], 
                              capture_output=True, text=True, timeout=60)
        
        return jsonify({
            "success": True,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "output": result.stdout,
            "error": result.stderr if result.stderr else None
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "error": str(e)
        })

@app.route('/status')
def status():
    """Status endpoint"""
    try:
        # Try to read last check time from a file
        try:
            with open('last_check.txt', 'r') as f:
                last_check = f.read().strip()
        except:
            last_check = "Never"
        
        return jsonify({
            "status": "running",
            "last_check": last_check,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
