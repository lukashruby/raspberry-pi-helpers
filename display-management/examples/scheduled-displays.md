# Scheduled Display Management Examples

This document provides practical examples of how to use the display management service with systemd for automation and scheduling.

## Basic Service Usage

### Manual Display Control

```bash
# Turn off a display immediately
systemctl --user start wlr-display-off@HDMI-A-1

# Turn on a display immediately
systemctl --user start wlr-display-on@HDMI-A-1

# Check service status
systemctl --user status wlr-display-off@HDMI-A-1
```

### Automatic Display Control at Login

```bash
# Turn off secondary display automatically when user logs in
systemctl --user enable wlr-display-off@HDMI-A-2

# Turn on primary display automatically when user logs in
systemctl --user enable wlr-display-on@HDMI-A-1
```

## Scheduled Operations

### Nightly Display Shutdown

Set up automatic display shutdown every night at 10 PM:

```bash
# Enable the nightly timer
systemctl --user enable --now wlr-display-off-nightly@HDMI-A-1.timer

# Check timer status
systemctl --user list-timers

# View timer logs
journalctl --user -u wlr-display-off-nightly@HDMI-A-1.timer
```

### Custom Timer Examples

Create custom timers for different schedules:

#### Morning Display Wake-up

```bash
# Create a custom morning timer
cat > ~/.config/systemd/user/wlr-display-morning@.timer <<'EOF'
[Unit]
Description=Turn ON output %i in the morning

[Timer]
OnCalendar=08:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Create corresponding service
cat > ~/.config/systemd/user/wlr-display-morning@.service <<'EOF'
[Unit]
Description=Turn ON output %i in the morning

[Service]
Type=oneshot
ExecStart=/usr/local/bin/wlr-display on %i
User=%i
EOF

# Enable the timer
systemctl --user daemon-reload
systemctl --user enable --now wlr-display-morning@HDMI-A-1.timer
```

#### Lunch Break Display Off

```bash
# Turn off displays during lunch break (12:00-13:00)
cat > ~/.config/systemd/user/wlr-display-lunch-off@.timer <<'EOF'
[Unit]
Description=Turn OFF output %i for lunch break

[Timer]
OnCalendar=12:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

cat > ~/.config/systemd/user/wlr-display-lunch-off@.service <<'EOF'
[Unit]
Description=Turn OFF output %i for lunch break

[Service]
Type=oneshot
ExecStart=/usr/local/bin/wlr-display off %i
User=%i
EOF

# Enable lunch break timer
systemctl --user daemon-reload
systemctl --user enable --now wlr-display-lunch-off@HDMI-A-1.timer
```

## Advanced Automation

### Power Management Integration

Create a script that turns off displays before system suspend:

```bash
# Create power management script
cat > ~/bin/display-power-manager.sh <<'EOF'
#!/bin/bash
# Turn off all displays before suspend
wlr-display off HDMI-A-1 HDMI-A-2
systemctl suspend
EOF

chmod +x ~/bin/display-power-manager.sh

# Create systemd service for power management
cat > ~/.config/systemd/user/display-power-manager.service <<'EOF'
[Unit]
Description=Display Power Manager
Before=sleep.target

[Service]
Type=oneshot
ExecStart=/home/%i/bin/display-power-manager.sh
RemainAfterExit=yes

[Install]
WantedBy=sleep.target
EOF

# Enable the service
systemctl --user enable display-power-manager.service
```

### SSH Remote Control

Create a simple web interface or API for remote control:

```bash
# Create a simple HTTP server script
cat > ~/bin/display-api.sh <<'EOF'
#!/bin/bash
# Simple HTTP API for display control
# Usage: ./display-api.sh <port>

PORT=${1:-8080}

while true; do
    {
        echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        echo "<html><body>"
        echo "<h1>Display Control</h1>"
        echo "<a href='/off/HDMI-A-1'>Turn Off HDMI-A-1</a><br>"
        echo "<a href='/on/HDMI-A-1'>Turn On HDMI-A-1</a><br>"
        echo "<a href='/toggle/HDMI-A-1'>Toggle HDMI-A-1</a><br>"
        echo "<a href='/list'>List Displays</a><br>"
        echo "</body></html>"
    } | nc -l -p $PORT -q 1
done
EOF

chmod +x ~/bin/display-api.sh
```

## Troubleshooting Scheduled Services

### Check Service Status

```bash
# List all user services
systemctl --user list-units

# Check specific service status
systemctl --user status wlr-display-off@HDMI-A-1

# View service logs
journalctl --user -u wlr-display-off@HDMI-A-1
```

### Enable User Lingering

For services to run without user login:

```bash
# Enable lingering for current user
sudo loginctl enable-linger $USER

# Check lingering status
loginctl show-user $USER | grep Linger
```

### Debug Timer Issues

```bash
# List all timers
systemctl --user list-timers --all

# Check timer status
systemctl --user status wlr-display-off-nightly@HDMI-A-1.timer

# View timer logs
journalctl --user -u wlr-display-off-nightly@HDMI-A-1.timer
```

## Best Practices

1. **Test Services Manually First**: Always test services with `systemctl --user start` before enabling them
2. **Use Descriptive Names**: Name your custom services clearly (e.g., `wlr-display-morning@`)
3. **Check Logs Regularly**: Monitor service logs to ensure they're working correctly
4. **Enable Lingering**: For headless systems, enable user lingering so services run without login
5. **Backup Configurations**: Keep copies of your custom service files in version control

## Common Use Cases

- **Home Theater PC**: Turn off displays when not in use, turn on for scheduled viewing
- **Digital Signage**: Schedule displays to turn on/off for business hours
- **Development Workstation**: Turn off secondary displays during focus time
- **Energy Saving**: Automatically turn off displays during off-hours
- **Remote Management**: Control displays via SSH or web interface
