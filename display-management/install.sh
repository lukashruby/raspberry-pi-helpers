#!/usr/bin/env bash
set -euo pipefail

# Display Management Service Installation Script
# Installs the wlr-display CLI tool for managing Wayland displays

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PATH="/usr/local/bin/wlr-display"

echo "Installing Display Management Service..."

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    echo "Error: This script should not be run as root directly."
    echo "Please run: sudo $0"
    exit 1
fi

# Check if sudo is available
if ! command -v sudo >/dev/null 2>&1; then
    echo "Error: sudo is required but not available"
    exit 1
fi

# Install wlr-randr if not present
echo "Checking for wlr-randr..."
if ! command -v wlr-randr >/dev/null 2>&1; then
    echo "wlr-randr not found. Installing..."
    sudo apt update
    sudo apt install -y wlr-randr
    echo "wlr-randr installed successfully"
else
    echo "wlr-randr is already installed"
fi

# Install the CLI script
echo "Installing wlr-display CLI..."
sudo cp "$SCRIPT_DIR/wlr-display" "$INSTALL_PATH"
sudo chmod +x "$INSTALL_PATH"

# Verify installation
if [[ -x "$INSTALL_PATH" ]]; then
    echo "✓ wlr-display installed successfully to $INSTALL_PATH"
else
    echo "✗ Installation failed"
    exit 1
fi

# Test the installation
echo "Testing installation..."
if "$INSTALL_PATH" --help >/dev/null 2>&1; then
    echo "✓ Installation test passed"
else
    echo "⚠ Installation test failed, but the script was installed"
fi

echo ""
echo "Installation complete!"
echo ""
echo "Usage examples:"
echo "  wlr-display list                    # List available displays"
echo "  wlr-display off HDMI-A-1            # Turn off a display"
echo "  wlr-display on HDMI-A-1             # Turn on a display"
echo "  wlr-display toggle HDMI-A-1         # Toggle display state"
echo ""
echo "For more information, see the README.md file."
