#!/bin/bash
set -e

echo "Installing display control system..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOTE_USER="lukas"
REMOTE_HOST="raspberry-pi"
REMOTE_DIR="/home/lukas/display-control"

# Create remote directory
echo "Creating remote directory..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ${REMOTE_DIR}"

# Copy files to Raspberry Pi
echo "Copying files to Raspberry Pi..."
scp ${SCRIPT_DIR}/display_web_service.py ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/
scp ${SCRIPT_DIR}/requirements.txt ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/
scp ${SCRIPT_DIR}/display-scheduled-off.service ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/
scp ${SCRIPT_DIR}/display-scheduled-on.service ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/
scp ${SCRIPT_DIR}/display-scheduled-off.timer ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/
scp ${SCRIPT_DIR}/display-scheduled-on.timer ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/
scp ${SCRIPT_DIR}/display-web.service ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/

# Install Python dependencies in virtual environment
echo "Installing Python dependencies in virtual environment..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo apt-get update && sudo apt-get install -y python3-venv || true"
ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_DIR} && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

# Install systemd timer services (user-level)
echo "Installing scheduled display control timers..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ~/.config/systemd/user"
ssh ${REMOTE_USER}@${REMOTE_HOST} "cp ${REMOTE_DIR}/display-scheduled-off.service ~/.config/systemd/user/"
ssh ${REMOTE_USER}@${REMOTE_HOST} "cp ${REMOTE_DIR}/display-scheduled-on.service ~/.config/systemd/user/"
ssh ${REMOTE_USER}@${REMOTE_HOST} "cp ${REMOTE_DIR}/display-scheduled-off.timer ~/.config/systemd/user/"
ssh ${REMOTE_USER}@${REMOTE_HOST} "cp ${REMOTE_DIR}/display-scheduled-on.timer ~/.config/systemd/user/"

# Enable and start timers
echo "Enabling and starting timers..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "systemctl --user daemon-reload"
ssh ${REMOTE_USER}@${REMOTE_HOST} "systemctl --user enable display-scheduled-off.timer"
ssh ${REMOTE_USER}@${REMOTE_HOST} "systemctl --user enable display-scheduled-on.timer"
ssh ${REMOTE_USER}@${REMOTE_HOST} "systemctl --user start display-scheduled-off.timer"
ssh ${REMOTE_USER}@${REMOTE_HOST} "systemctl --user start display-scheduled-on.timer"

# Install web service (system-level, needs sudo for port 80)
echo "Installing web service..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo cp ${REMOTE_DIR}/display-web.service /etc/systemd/system/"
ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo systemctl daemon-reload"
ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo systemctl enable display-web.service"
ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo systemctl start display-web.service"

echo ""
echo "Installation complete!"
echo ""
echo "Scheduled display control:"
echo "  - Displays will turn OFF at 19:00 daily (HDMI-A-2 first, then HDMI-A-1)"
echo "  - Displays will turn ON at 7:30 daily (HDMI-A-1 first, then HDMI-A-2)"
echo ""
echo "Web service:"
echo "  - Access at: http://raspberry-pi/"
echo "  - Check status: sudo systemctl status display-web.service"
echo ""
echo "To check timer status:"
echo "  systemctl --user list-timers"

