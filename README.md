# NetConnect - Cross-Platform TCP/UDP Connection Testing Tool

NetConnect is a modern, cross-platform command-line tool for creating TCP/UDP port listeners and testing connectivity to remote servers across IP ranges. Written in Python 3.10+ with single-codebase architecture.

## Features

- **Cross-platform single binary** - Linux, Windows, macOS (x64/ARM64)
- **Port listeners** - Create TCP/UDP listeners on multiple ports
- **Connection testing** - Test connectivity to IP ranges and port combinations
- **Multiple output formats** - Table (default), JSON, CSV
- **Persistent configuration** - YAML config file with sensible defaults
- **Real socket operations** - TCP connect with latency, UDP datagram testing, listener sockets
- **Platform-native installers** - DEB/RPM/AppImage, EXE/MSI, PKG/DMG

## Quick Start

### Download Portable Binary
```bash
# Linux
wget https://github.com/DavoudTeimouri/NetConnect-Tool/releases/latest/download/netconnect
chmod +x netconnect

# Or build from source
git clone https://github.com/DavoudTeimouri/NetConnect-Tool
cd NetConnect-Tool
./scripts/build_portable.py
```

### Install via Package Manager
```bash
# Debian/Ubuntu
sudo dpkg -i netconnect_2.0.0_amd64.deb

# RHEL/Fedora
sudo rpm -i netconnect-2.0.0-1.x86_64.rpm

# Windows
netconnect-2.0.0-setup.exe

# macOS
sudo installer -pkg NetConnect-2.0.0.pkg -target /
```

## Usage

### Create Port Listeners
```bash
# Listen on TCP/UDP ports 8080 and 9000 for 60 seconds
netconnect listen -p 8080 9000 --duration 60

# TCP only
netconnect listen -p 8080 9000 --protocol tcp

# UDP only
netconnect listen -p 53 --protocol udp
```

### Test Connections
```bash
# Test TCP ports 22, 80, 443 on IP range
netconnect test -t 192.168.1.100-192.168.1.110 -p 22 80 443

# Test with UDP only, JSON output
netconnect test -t 10.0.0.1-10.0.0.10 -p 53 --protocol udp --output json

# Single IP, CSV output
netconnect test -t 192.168.1.1 -p 22 80 443 --output csv
```

### Configuration
```bash
# Show config file path
netconnect config show-path

# Show current config
netconnect config show

# Set defaults
netconnect config set defaults.duration 60
netconnect config set defaults.timeout 10
netconnect config set defaults.output json
netconnect config set defaults.protocol tcp

# Reset to defaults
netconnect config reset
```

## Configuration File

Location:
- **Linux/macOS**: `~/.config/netconnect/config.yaml`
- **Windows**: `%APPDATA%\netconnect\config.yaml`

```yaml
defaults:
  duration: 300      # Default listener duration (seconds)
  timeout: 5         # Connection timeout (seconds)
  output: table      # Output format: table | json | csv
  protocol: both     # Protocol: tcp | udp | both

logging:
  level: INFO        # DEBUG | INFO | WARNING | ERROR
  file: ""           # Log file path (empty = stderr)
```

## Command Reference

### `netconnect listen`
Create TCP/UDP port listeners.

| Option | Description |
|--------|-------------|
| `-p, --ports PORTS` | Ports to listen on (required) |
| `--protocol` | tcp, udp, or both (default: both) |
| `--duration SEC` | Duration to run (default: indefinite) |
| `--host HOST` | Bind address (default: 0.0.0.0) |

### `netconnect test`
Test connections to target IPs and ports.

| Option | Description |
|--------|-------------|
| `-t, --targets RANGE` | IP range (e.g., 192.168.1.100-192.168.1.110) |
| `-p, --ports PORTS` | Ports to test (required) |
| `--protocol` | tcp, udp, or both (default: both) |
| `--timeout SEC` | Connection timeout (default: 5s) |
| `--output FORMAT` | table, json, or csv (default: table) |

### `netconnect config`
Manage configuration.

| Subcommand | Description |
|------------|-------------|
| `show` | Display current configuration |
| `show-path` | Show config file path |
| `reset` | Reset to defaults |
| `set KEY VALUE` | Set config value (e.g., `defaults.duration 60`) |

## Requirements

- **Runtime**: None (single portable executable)
- **Build**: Python 3.10+, PyInstaller
- **Dependencies** (bundled): platformdirs, pyyaml, tabulate

## Building from Source

```bash
# Install build dependencies
pip install -e ".[build]"

# Build portable executable
./scripts/build_portable.py

# Output: dist/netconnect (or netconnect.exe on Windows)
```

### Platform-Specific Installers

```bash
# Linux DEB
dpkg-deb --build packaging/linux/debian

# Linux RPM
rpmbuild -ba packaging/linux/rpm/netconnect.spec

# Windows EXE (Inno Setup)
iscc packaging/windows/inno/netconnect.iss

# Windows MSI (WiX)
msbuild packaging/windows/msi/netconnect.wixproj

# macOS PKG
pkgbuild --root staging --identifier com.netconnect.tool --version 2.0.0 NetConnect-2.0.0.pkg

# macOS DMG
create-dmg --volname "NetConnect" NetConnect-2.0.0.dmg staging/
```

## Project Structure

```
NetConnect-Tool/
├── src/netconnect/
│   ├── __init__.py       # Package metadata
│   ├── cli.py            # CLI entry point
│   ├── core.py           # Socket logic, IP parsing
│   └── config.py         # Configuration management
├── tests/
│   └── test_core.py      # Unit tests
├── packaging/
│   ├── linux/            # DEB, RPM, AppImage
│   ├── windows/          # Inno Setup, WiX/MSI
│   └── macos/            # pkgbuild, create-dmg
├── scripts/
│   └── build_portable.py # PyInstaller wrapper
├── pyproject.toml        # Modern packaging config
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

- **v2.0.0** - Cross-platform redesign, single Python codebase, portable binaries, platform-native installers
- **v1.1.0** - Network hop checking, auto-shutdown, duration option
- **v1.0.0** - Initial release (Bash, Perl, Python, PowerShell)