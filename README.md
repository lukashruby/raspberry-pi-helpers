# Raspberry Pi Display Control System

This project provides automated and web-based control for Raspberry Pi displays connected via HDMI.

## Features

1. **Scheduled Display Control**: Automatically turns displays off at 19:00 and on at 7:30 daily
2. **Web Interface**: Simple web UI with buttons to control displays (runs on port 80)

## Installation

Run the installation script from your local machine:

```bash
./install.sh
```

This will:
- Copy all necessary files to the Raspberry Pi
- Install `python3-venv` if needed
- Create a Python virtual environment
- Install Python dependencies (Flask) in the virtual environment
- Set up systemd timer services for scheduled control
- Set up systemd service for the web interface
- Enable and start all services

**Note**: The installation script requires SSH access to the Raspberry Pi. Make sure you can SSH into `raspberry-pi` as user `lukas` without a password prompt (or use SSH keys).

## Components

### Scheduled Display Control

**Services**:
- `display-scheduled-off.service` - Turns off displays (HDMI-A-2 first, then HDMI-A-1)
- `display-scheduled-on.service` - Turns on displays (HDMI-A-1 first, then HDMI-A-2)
- `display-scheduled-off.timer` - Triggers at 19:00 daily
- `display-scheduled-on.timer` - Triggers at 7:30 daily

**Location**: `~/.config/systemd/user/` (user-level services)

**Commands**:
```bash
# Check timer status
systemctl --user list-timers

# Check service status
systemctl --user status display-scheduled-off.service
systemctl --user status display-scheduled-on.service

# Manually trigger services
systemctl --user start display-scheduled-off.service
systemctl --user start display-scheduled-on.service
```

### Web Service

**Service**: `display-web.service` (system-level, runs on port 80)

**Location**: `/etc/systemd/system/display-web.service`

**Application Location**: `/home/lukas/display-control/`

**Virtual Environment**: `/home/lukas/display-control/venv/`

**Access**: Open `http://raspberry-pi/` in your browser

**Features**:
- Turn all displays on immediately
- Turn all displays on for 1 hour (auto-off after 1 hour)
- Turn all displays off immediately
- Modern, responsive web interface
- Real-time status updates

**Commands**:
```bash
# Check service status
sudo systemctl status display-web.service

# View logs
sudo journalctl -u display-web.service -f

# Restart service
sudo systemctl restart display-web.service
```

## Display Control Order

When turning displays **OFF**:
1. HDMI-A-2 (second display) - turned off first
2. HDMI-A-1 (first display) - turned off second

When turning displays **ON**:
1. HDMI-A-1 (first display) - turned on first
2. HDMI-A-2 (second display) - turned on second

## Manual Control

You can also control displays manually using the existing services:

```bash
# Turn displays on/off individually
systemctl --user start wlr-display-on@HDMI-A-1
systemctl --user start wlr-display-on@HDMI-A-2
systemctl --user start wlr-display-off@HDMI-A-1
systemctl --user start wlr-display-off@HDMI-A-2

# Or use the wlr-display script directly
wlr-display on HDMI-A-1
wlr-display off HDMI-A-2
wlr-display list
```

## Troubleshooting

### Web service not accessible
- Check if service is running: `sudo systemctl status display-web.service`
- Check if port 80 is in use: `sudo netstat -tlnp | grep :80` or `sudo ss -tlnp | grep :80`
- Check logs: `sudo journalctl -u display-web.service -n 50`
- Verify virtual environment exists: `ls -la /home/lukas/display-control/venv/`
- Test Python script manually: `sudo /home/lukas/display-control/venv/bin/python3 /home/lukas/display-control/display_web_service.py`

### Scheduled timers not working
- Check timer status: `systemctl --user list-timers`
- Check if user systemd is running: `systemctl --user status`
- Check service logs: `journalctl --user -u display-scheduled-off.service`

### Display commands not working
- Verify user systemd services exist: `systemctl --user list-unit-files | grep wlr-display`
- Check if wlr-randr is installed: `which wlr-randr`
- Test manually: `wlr-display list`

## Files

- `display-scheduled-off.service` - Service to turn displays off
- `display-scheduled-on.service` - Service to turn displays on
- `display-scheduled-off.timer` - Timer for 19:00 daily
- `display-scheduled-on.timer` - Timer for 7:30 daily
- `display_web_service.py` - Flask web application
- `display-web.service` - Systemd service for web app
- `requirements.txt` - Python dependencies
- `install.sh` - Installation script

## Requirements

- Raspberry Pi with 2 HDMI displays
- Wayland/WLR-RandR setup (existing `wlr-display` script)
- Python 3 with `python3-venv` package
- Flask (installed in virtual environment via requirements.txt)
- User-level systemd services for display control (already set up)
- SSH access to Raspberry Pi (passwordless recommended)

## Installation Details

The web service runs in a Python virtual environment to avoid conflicts with system-managed Python packages. The virtual environment is automatically created during installation at `/home/lukas/display-control/venv/`.

The systemd service runs as root (to bind to port 80) but executes commands as user `lukas` to access user-level systemd services for display control.

## Updating

To update the web service after making changes:

```bash
# Copy updated files
scp display_web_service.py lukas@raspberry-pi:/home/lukas/display-control/
scp requirements.txt lukas@raspberry-pi:/home/lukas/display-control/

# Update dependencies if needed
ssh lukas@raspberry-pi "cd /home/lukas/display-control && source venv/bin/activate && pip install -r requirements.txt"

# Restart the service
ssh lukas@raspberry-pi "sudo systemctl restart display-web.service"
```

