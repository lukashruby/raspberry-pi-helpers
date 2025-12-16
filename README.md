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
- **Web interface** for remote display control (runs on port 80)
- **Daily scheduled timers** (auto-off at 19:00, auto-on at 7:30)

**Requirements:**
- Raspberry Pi with Wayland (typically Raspberry Pi OS with desktop)
- `wlr-randr` package

## Quick Start

### Display Management

1. **Install the display management CLI:**
   ```bash
   cd display-management
   sudo ./install.sh
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
   cd display-management
   ./setup-services.sh
   ```

4. **Web Service (Optional):**
   ```bash
   # Configure connection settings (optional, defaults provided)
   cd display-management/web-service
   cp .env.example .env
   # Edit .env with your Raspberry Pi connection details
   
   # Install and start the web service for remote control
   ./install.sh
   ```
   Access the web interface at `http://<your-raspberry-pi-host>/`

5. **Scheduled Display Control (Optional):**
   ```bash
   # Set up daily timers (off at 19:00, on at 7:30)
   cd display-management
   # Copy timer services to ~/.config/systemd/user/
   cp systemd/display-scheduled-*.{service,timer} ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable --now display-scheduled-off.timer
   systemctl --user enable --now display-scheduled-on.timer
   ```

## Project Structure

```
raspberry-pi-helpers/
├── README.md                           # This file
├── LICENSE                             # MIT License
├── display-management/                 # Display management helper
│   ├── README.md                      # Detailed documentation
│   ├── display-setup.md               # Setup documentation
│   ├── install.sh                     # CLI installation script
│   ├── setup-services.sh              # Systemd services setup
│   ├── wlr-display                    # Main CLI script
│   ├── systemd/                       # Systemd service templates
│   │   ├── wlr-display-off@.service
│   │   ├── wlr-display-on@.service
│   │   ├── wlr-display-off-nightly@.service
│   │   ├── wlr-display-off-nightly@.timer
│   │   ├── display-scheduled-off.service
│   │   ├── display-scheduled-on.service
│   │   ├── display-scheduled-off.timer
│   │   └── display-scheduled-on.timer
│   ├── web-service/                   # Web interface
│   │   ├── display_web_service.py    # Flask web application
│   │   ├── display-web.service        # Systemd service
│   │   ├── requirements.txt           # Python dependencies
│   │   └── install.sh                 # Installation script
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
