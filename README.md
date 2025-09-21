# Raspberry Pi Helpers

A collection of useful utilities and services for Raspberry Pi systems, designed to make common tasks easier and more automated.

## Available Helpers

### 1. Display Management Service

A comprehensive solution for managing Wayland displays on Raspberry Pi, allowing you to turn displays on/off via SSH and optionally schedule display operations.

**Features:**
- Turn displays on/off via command line
- Toggle display states
- List available displays
- Set specific display modes
- SSH-friendly (no manual Wayland socket configuration needed)
- Optional systemd service integration
- Scheduled display operations with timers

**Requirements:**
- Raspberry Pi with Wayland (typically Raspberry Pi OS with desktop)
- `wlr-randr` package

## Quick Start

### Display Management

1. **Install the display management CLI:**
   ```bash
   sudo ./install-display-service.sh
   ```

2. **Basic usage:**
   ```bash
   # List available displays
   wlr-display list
   
   # Turn off a display
   wlr-display off HDMI-A-1
   
   # Turn on a display with specific mode
   wlr-display on HDMI-A-1 --mode 1920x1080@60
   
   # Toggle display state
   wlr-display toggle HDMI-A-1
   ```

3. **Optional: Set up systemd services for automation:**
   ```bash
   ./setup-display-services.sh
   ```

## Project Structure

```
rpi5-helpers/
├── README.md                           # This file
├── LICENSE                             # MIT License
├── display-management/                 # Display management helper
│   ├── README.md                      # Detailed documentation
│   ├── install.sh                     # Installation script
│   ├── wlr-display                    # Main CLI script
│   ├── systemd/                       # Systemd service templates
│   │   ├── wlr-display-off@.service
│   │   ├── wlr-display-on@.service
│   │   ├── wlr-display-off-nightly@.service
│   │   └── wlr-display-off-nightly@.timer
│   └── examples/                      # Usage examples
│       └── scheduled-displays.md
└── CONTRIBUTING.md                    # Contribution guidelines
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
