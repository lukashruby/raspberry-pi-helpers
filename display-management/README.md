# Display Management Service

A comprehensive solution for managing Wayland displays on Raspberry Pi systems. This helper allows you to control displays via command line, making it perfect for remote management via SSH and automation scenarios.

## Features

- **Command Line Control**: Turn displays on/off, toggle states, and set specific modes
- **SSH Friendly**: Automatically detects and uses the correct Wayland socket
- **Display Listing**: See all available displays and their current states
- **Systemd Integration**: Optional service templates for automation
- **Scheduling**: Built-in timer support for scheduled display operations
- **Multi-Display Support**: Control multiple displays simultaneously

## Requirements

- Raspberry Pi with Wayland (typically Raspberry Pi OS with desktop environment)
- `wlr-randr` package
- User with access to Wayland session

## Installation

### Quick Install

```bash
sudo ./install.sh
```

This will:
- Install the `wlr-display` command to `/usr/local/bin/`
- Make it executable
- Verify `wlr-randr` is available

### Manual Install

```bash
# Install wlr-randr if not present
sudo apt update && sudo apt install wlr-randr

# Copy the script
sudo cp wlr-display /usr/local/bin/
sudo chmod +x /usr/local/bin/wlr-display
```

## Usage

### Basic Commands

```bash
# List all available displays
wlr-display list

# Turn off a display
wlr-display off HDMI-A-1

# Turn on a display
wlr-display on HDMI-A-1

# Turn on with specific mode
wlr-display on HDMI-A-1 --mode 1920x1080@60

# Toggle display state
wlr-display toggle HDMI-A-1

# Control multiple displays
wlr-display off HDMI-A-1 HDMI-A-2
wlr-display on HDMI-A-1 HDMI-A-2 --mode 1920x1080@60
```

### Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `list` | Show all available displays and their states | `wlr-display list` |
| `off <outputs>` | Turn off specified displays | `wlr-display off HDMI-A-1` |
| `on <outputs> [--mode <mode>]` | Turn on displays with optional mode | `wlr-display on HDMI-A-1 --mode 1920x1080@60` |
| `toggle <outputs>` | Toggle display states | `wlr-display toggle HDMI-A-1` |

### Finding Display Names

Use `wlr-display list` to see available outputs. Common names include:
- `HDMI-A-1`, `HDMI-A-2` (HDMI ports)
- `DSI-1` (built-in display)
- `Composite-1` (composite video)

## Systemd Integration

### Setting Up Services

The helper includes systemd service templates for automation:

```bash
# Set up systemd services
./setup-services.sh
```

This creates user services that can be triggered manually or enabled for automatic execution.

### Manual Service Setup

```bash
# Create systemd user directory
mkdir -p ~/.config/systemd/user

# Copy service templates
cp systemd/*.service ~/.config/systemd/user/
cp systemd/*.timer ~/.config/systemd/user/

# Reload systemd
systemctl --user daemon-reload
```

### Using Services

```bash
# Turn off a display
systemctl --user start wlr-display-off@HDMI-A-1

# Turn on a display
systemctl --user start wlr-display-on@HDMI-A-1

# Enable automatic display off at login
systemctl --user enable wlr-display-off@HDMI-A-2
```

### Scheduled Operations

Set up a nightly display shutdown:

```bash
# Enable the nightly timer
systemctl --user enable --now wlr-display-off-nightly@HDMI-A-1.timer

# Check timer status
systemctl --user list-timers
```

## Examples

See the [examples directory](examples/) for common use cases and automation scenarios.

## Troubleshooting

### "wlr-randr not found"
```bash
sudo apt update && sudo apt install wlr-randr
```

### "No Wayland display socket found"
- Ensure you're running a Wayland session (not X11)
- Check that the desktop environment is running
- Try logging in via the desktop interface first

### "Output not found"
- Use `wlr-display list` to see available outputs
- Check that the display is physically connected
- Verify the display is powered on

### Services not working
- Ensure user lingering is enabled: `sudo loginctl enable-linger $USER`
- Check service status: `systemctl --user status wlr-display-off@HDMI-A-1`
- Verify the user session is active

## Advanced Usage

### Custom Display Modes

```bash
# Set custom resolution and refresh rate
wlr-display on HDMI-A-1 --mode 2560x1440@75

# Use preferred mode (default)
wlr-display on HDMI-A-1
```

### SSH Automation

Perfect for remote management:

```bash
# From another machine
ssh pi@raspberrypi.local "wlr-display off HDMI-A-1"
ssh pi@raspberrypi.local "wlr-display on HDMI-A-1 --mode 1920x1080@60"
```

### Script Integration

```bash
#!/bin/bash
# Example: Turn off displays before sleep
wlr-display off HDMI-A-1 HDMI-A-2
systemctl suspend
```

## Contributing

Found a bug or have a feature request? Please open an issue or submit a pull request following our [contribution guidelines](../../CONTRIBUTING.md).
