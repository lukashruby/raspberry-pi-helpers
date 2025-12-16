# Contributing to Raspberry Pi Helpers

Thank you for your interest in contributing to this project! This document provides guidelines for contributing new helpers and improving existing ones.

## How to Contribute

### 1. Fork and Clone
1. Fork this repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or fix

### 2. Adding a New Helper

When adding a new helper, please follow this structure:

```
helpers/
├── your-helper-name/
│   ├── README.md              # Detailed documentation
│   ├── install.sh             # Installation script
│   ├── main-script            # Main executable
│   ├── systemd/               # Systemd services (if applicable)
│   └── examples/              # Usage examples
```

### 3. Documentation Requirements

Each helper must include:
- **README.md**: Comprehensive documentation with:
  - Purpose and features
  - Requirements and dependencies
  - Installation instructions
  - Usage examples
  - Troubleshooting section
- **Install script**: Automated installation process
- **Examples**: Real-world usage scenarios

### 4. Code Standards

- Use bash for shell scripts with `set -euo pipefail`
- Include proper error handling and user feedback
- Add comments explaining complex logic
- Follow existing naming conventions
- Test on actual Raspberry Pi hardware when possible

### 5. Testing

Before submitting:
- Test the installation script
- Verify all functionality works as documented
- Test error conditions and edge cases
- Ensure scripts work over SSH

### 6. Pull Request Process

1. Update the main README.md to include your new helper
2. Ensure all documentation is complete
3. Test thoroughly
4. Submit a pull request with a clear description

## Helper Categories

We're looking for helpers in these areas:
- **System Management**: Services, automation, monitoring
- **Hardware Control**: GPIO, sensors, peripherals
- **Network**: WiFi, Bluetooth, connectivity
- **Media**: Audio, video, streaming
- **Development**: Build tools, deployment, testing

## Questions?

If you have questions about contributing, please open an issue or start a discussion.
