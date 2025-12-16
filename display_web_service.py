#!/usr/bin/env python3
"""
Web service for controlling Raspberry Pi displays via HTTP API.
Runs on port 80 and provides a simple web interface with buttons.
"""

import os
import subprocess
import threading
import time
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request
from werkzeug.serving import make_server

app = Flask(__name__)

# Track scheduled turn-off time
scheduled_off_time = None
scheduled_off_timer = None
scheduled_off_lock = threading.Lock()


def run_display_command(action, display):
    """Run display control command via systemctl --user as user 'lukas'"""
    try:
        # Run as user 'lukas' to access user-level systemd services
        # Use su with proper environment to access user's systemd session
        service_name = f'wlr-display-{action}@{display}'
        cmd = [
            'su', '-l', 'lukas', '-c',
            f'XDG_RUNTIME_DIR=/run/user/1000 systemctl --user start {service_name}'
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            print(f"Error running {cmd}: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running display command: {e}")
        return False


def turn_all_displays(action):
    """Turn all displays on or off"""
    if action == 'on':
        # Turn on HDMI-A-1 first, then HDMI-A-2
        success1 = run_display_command('on', 'HDMI-A-1')
        time.sleep(0.5)
        success2 = run_display_command('on', 'HDMI-A-2')
    else:  # off
        # Turn off HDMI-A-2 first, then HDMI-A-1
        success2 = run_display_command('off', 'HDMI-A-2')
        time.sleep(0.5)
        success1 = run_display_command('off', 'HDMI-A-1')
    
    return success1 and success2


def cancel_scheduled_off():
    """Cancel any scheduled turn-off"""
    global scheduled_off_time, scheduled_off_timer
    with scheduled_off_lock:
        if scheduled_off_timer:
            scheduled_off_timer.cancel()
            scheduled_off_timer = None
        scheduled_off_time = None


def schedule_turn_off(hours=1):
    """Schedule displays to turn off in specified hours"""
    global scheduled_off_time, scheduled_off_timer
    
    cancel_scheduled_off()
    
    turn_off_time = datetime.now() + timedelta(hours=hours)
    
    def turn_off_callback():
        turn_all_displays('off')
        with scheduled_off_lock:
            global scheduled_off_time, scheduled_off_timer
            scheduled_off_time = None
            scheduled_off_timer = None
    
    delay_seconds = (turn_off_time - datetime.now()).total_seconds()
    
    with scheduled_off_lock:
        scheduled_off_time = turn_off_time
        scheduled_off_timer = threading.Timer(delay_seconds, turn_off_callback)
        scheduled_off_timer.start()
    
    return turn_off_time


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Display Control</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 500px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .button-group {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        button {
            padding: 18px 30px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        button:active {
            transform: translateY(0);
        }
        .btn-on {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-on-1h {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .btn-off {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        .status {
            margin-top: 25px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 10px;
            text-align: center;
            font-size: 14px;
            color: #666;
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
        }
        .scheduled-info {
            margin-top: 15px;
            padding: 12px;
            background: #e7f3ff;
            border-radius: 8px;
            font-size: 13px;
            color: #004085;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖥️ Display Control</h1>
        <p class="subtitle">Control your Raspberry Pi displays</p>
        
        <div class="button-group">
            <button class="btn-on" onclick="turnOn()">Turn All Displays On</button>
            <button class="btn-on-1h" onclick="turnOnFor1Hour()">Turn On For 1 Hour</button>
            <button class="btn-off" onclick="turnOff()">Turn All Displays Off</button>
        </div>
        
        <div id="status" class="status">Ready</div>
        <div id="scheduled" class="scheduled-info" style="display: none;"></div>
    </div>

    <script>
        function updateStatus(message, isSuccess = true) {
            const statusEl = document.getElementById('status');
            statusEl.textContent = message;
            statusEl.className = 'status ' + (isSuccess ? 'success' : 'error');
            setTimeout(() => {
                statusEl.textContent = 'Ready';
                statusEl.className = 'status';
            }, 3000);
        }

        function updateScheduledInfo(timeStr) {
            const scheduledEl = document.getElementById('scheduled');
            if (timeStr) {
                scheduledEl.textContent = `Scheduled to turn off at: ${timeStr}`;
                scheduledEl.style.display = 'block';
            } else {
                scheduledEl.style.display = 'none';
            }
        }

        async function turnOn() {
            updateStatus('Turning displays on...', true);
            try {
                const response = await fetch('/api/displays/on', { method: 'POST' });
                const data = await response.json();
                if (data.success) {
                    updateStatus('Displays turned on successfully!', true);
                    updateScheduledInfo(null);
                } else {
                    updateStatus('Error: ' + (data.error || 'Failed to turn on displays'), false);
                }
            } catch (error) {
                updateStatus('Error: ' + error.message, false);
            }
        }

        async function turnOnFor1Hour() {
            updateStatus('Turning displays on for 1 hour...', true);
            try {
                const response = await fetch('/api/displays/on-1h', { method: 'POST' });
                const data = await response.json();
                if (data.success) {
                    updateStatus('Displays turned on! Will turn off in 1 hour.', true);
                    updateScheduledInfo(data.turn_off_time);
                } else {
                    updateStatus('Error: ' + (data.error || 'Failed to schedule'), false);
                }
            } catch (error) {
                updateStatus('Error: ' + error.message, false);
            }
        }

        async function turnOff() {
            updateStatus('Turning displays off...', true);
            try {
                const response = await fetch('/api/displays/off', { method: 'POST' });
                const data = await response.json();
                if (data.success) {
                    updateStatus('Displays turned off successfully!', true);
                    updateScheduledInfo(null);
                } else {
                    updateStatus('Error: ' + (data.error || 'Failed to turn off displays'), false);
                }
            } catch (error) {
                updateStatus('Error: ' + error.message, false);
            }
        }

        // Check for scheduled turn-off on page load
        async function checkScheduled() {
            try {
                const response = await fetch('/api/displays/scheduled');
                const data = await response.json();
                if (data.scheduled_time) {
                    updateScheduledInfo(data.scheduled_time);
                }
            } catch (error) {
                console.error('Error checking scheduled time:', error);
            }
        }

        checkScheduled();
        setInterval(checkScheduled, 30000); // Check every 30 seconds
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/displays/on', methods=['POST'])
def api_turn_on():
    """API endpoint to turn all displays on"""
    cancel_scheduled_off()
    success = turn_all_displays('on')
    return jsonify({'success': success})


@app.route('/api/displays/off', methods=['POST'])
def api_turn_off():
    """API endpoint to turn all displays off"""
    cancel_scheduled_off()
    success = turn_all_displays('off')
    return jsonify({'success': success})


@app.route('/api/displays/on-1h', methods=['POST'])
def api_turn_on_1h():
    """API endpoint to turn displays on for 1 hour"""
    success = turn_all_displays('on')
    if success:
        turn_off_time = schedule_turn_off(hours=1)
        return jsonify({
            'success': True,
            'turn_off_time': turn_off_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({'success': False, 'error': 'Failed to turn on displays'})


@app.route('/api/displays/scheduled', methods=['GET'])
def api_get_scheduled():
    """API endpoint to get scheduled turn-off time"""
    with scheduled_off_lock:
        if scheduled_off_time:
            return jsonify({
                'scheduled_time': scheduled_off_time.strftime('%Y-%m-%d %H:%M:%S')
            })
    return jsonify({'scheduled_time': None})


if __name__ == '__main__':
    print("Starting display control web service on port 80...")
    print("Access the interface at: http://raspberry-pi/")
    app.run(host='0.0.0.0', port=80, debug=False)

