# Raspberry Pi Display Control Setup

## Overview
The Raspberry Pi has 2 displays connected via HDMI, controlled through user-level systemd services using Wayland/WLR-RandR.

## Hardware
- **Display 1**: HDMI-A-1 - ChangHong Electric Co.,Ltd 22P610FS
- **Display 2**: HDMI-A-2 - ChangHong Electric Co.,Ltd 22P610FS
- Both displays support up to 1920x1080@75Hz
- Display 2 is rotated 180 degrees (Transform: 180)

## Components

### 1. Display Control Script
**Location**: `/usr/local/bin/wlr-display`

A bash script that wraps `wlr-randr` to control Wayland displays. It automatically detects the Wayland socket for the current user session.

**Usage**:
```bash
wlr-display list                    # List all displays
wlr-display off HDMI-A-1            # Turn off display
wlr-display on HDMI-A-1             # Turn on display
wlr-display on HDMI-A-1 --mode 1920x1080@60  # Turn on with specific mode
wlr-display toggle HDMI-A-1         # Toggle display state
```

### 2. Systemd User Services
**Location**: `~/.config/systemd/user/`

Two template services that allow controlling displays via systemd:

#### `wlr-display-off@.service`
Turns off a specified display.

**Usage**:
```bash
systemctl --user start wlr-display-off@HDMI-A-1
systemctl --user start wlr-display-off@HDMI-A-2
```

**Service file**:
```ini
[Unit]
Description=Turn OFF Wayland output %i
After=default.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/wlr-display off %i

[Install]
WantedBy=default.target
```

#### `wlr-display-on@.service`
Turns on a specified display with default mode 1920x1080@60.

**Usage**:
```bash
systemctl --user start wlr-display-on@HDMI-A-1
systemctl --user start wlr-display-on@HDMI-A-2
```

**Service file**:
```ini
[Unit]
Description=Turn ON Wayland output %i
After=default.target

[Service]
Type=oneshot
# Change the mode if you want a different default
ExecStart=/usr/local/bin/wlr-display on %i --mode 1920x1080@60

[Install]
WantedBy=default.target
```

## Common Commands

### Control displays
```bash
# Turn off both displays
systemctl --user start wlr-display-off@HDMI-A-1
systemctl --user start wlr-display-off@HDMI-A-2

# Turn on both displays
systemctl --user start wlr-display-on@HDMI-A-1
systemctl --user start wlr-display-on@HDMI-A-2

# Reload systemd after service changes
systemctl --user daemon-reload
```

### Check display status
```bash
wlr-randr                    # List all displays and their status
systemctl --user status wlr-display-off@HDMI-A-1
systemctl --user status wlr-display-on@HDMI-A-1
```

## Additional System Services

### `rp1-test.service`
System-level service that checks for RP1 displays and configures Xorg primary GPU.

**Purpose**: Automatically detects if RP1 displays (vec/dsi/dpi) are present on Raspberry Pi 5 and configures Xorg to use the appropriate primary GPU driver.

- **Location**: `/lib/systemd/system/rp1-test.service`
- **Script**: `/lib/systemd/scripts/rp1_test.sh`
- **Status**: Active (exited) - runs at boot
- **Target**: `multi-user.target`

**Service file**:
```ini
[Unit]
Description=Check for RP1 displays for Xorg

[Service]
Type=oneshot
ExecStart=/usr/lib/systemd/scripts/rp1_test.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

**Script logic**:
- Defaults to `vc4` driver for older Pi models
- On Pi 5, checks for vec/dsi/dpi displays
- If found, switches to `rp1` driver and updates Xorg config
- Creates/updates `/etc/X11/xorg.conf.d/99-v3d.conf`

### `rpi-display-backlight.service`
System-level service that turns off Raspberry Pi display backlight on shutdown/reboot.

- **Location**: `/lib/systemd/system/rpi-display-backlight.service`
- **Targets**: Linked to `reboot.target`, `halt.target`, and `poweroff.target`
- **Condition**: Only runs if `/proc/device-tree/rpi_backlight` exists

**Service file**:
```ini
[Unit]
Description=Turns off Raspberry Pi display backlight on shutdown/reboot
ConditionPathIsDirectory=/proc/device-tree/rpi_backlight
DefaultDependencies=no
Before=umount.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c '/bin/echo 1 > /sys/class/backlight/rpi_backlight/bl_power'

[Install]
WantedBy=reboot.target halt.target poweroff.target
```

## Display Information

Both displays are currently:
- **Enabled**: Yes
- **Current Mode**: 1920x1080@75Hz
- **Position**: HDMI-A-1 at (0,0), HDMI-A-2 at (0,1080) - stacked vertically
- **Transform**: HDMI-A-1 normal, HDMI-A-2 rotated 180°

## Notes
- Services are user-level (run with `systemctl --user`)
- The `wlr-display` script requires `wlr-randr` package
- Services use template syntax (`@`) to allow specifying display names as instances
- Both services are enabled but not started by default (oneshot services)

