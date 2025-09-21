#!/usr/bin/env bash
set -euo pipefail

# Systemd Services Setup Script
# Sets up systemd user services for display management automation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

echo "Setting up systemd services for display management..."

# Create systemd user directory if it doesn't exist
mkdir -p "$SYSTEMD_USER_DIR"

# Copy service files
echo "Installing service templates..."
cp "$SCRIPT_DIR/systemd"/*.service "$SYSTEMD_USER_DIR/"
cp "$SCRIPT_DIR/systemd"/*.timer "$SYSTEMD_USER_DIR/"

# Reload systemd user daemon
echo "Reloading systemd user daemon..."
systemctl --user daemon-reload

echo "✓ Systemd services installed successfully!"
echo ""
echo "Available services:"
echo "  wlr-display-off@<output>.service      # Turn off a specific display"
echo "  wlr-display-on@<output>.service       # Turn on a specific display"
echo "  wlr-display-off-nightly@<output>.timer # Nightly display shutdown timer"
echo ""
echo "Usage examples:"
echo "  # Turn off HDMI-A-1 display"
echo "  systemctl --user start wlr-display-off@HDMI-A-1"
echo ""
echo "  # Turn on HDMI-A-1 display"
echo "  systemctl --user start wlr-display-on@HDMI-A-1"
echo ""
echo "  # Enable automatic display off at login"
echo "  systemctl --user enable wlr-display-off@HDMI-A-2"
echo ""
echo "  # Set up nightly display shutdown at 10 PM"
echo "  systemctl --user enable --now wlr-display-off-nightly@HDMI-A-1.timer"
echo ""
echo "  # Check timer status"
echo "  systemctl --user list-timers"
echo ""
echo "Note: For services to run without user login, enable lingering:"
echo "  sudo loginctl enable-linger $USER"
