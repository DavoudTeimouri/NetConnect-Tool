# Change Log

## [2.0.0] - 2025-08-24

### Added
- Complete redesign as cross-platform single-codebase application (Python 3.10+)
- Single portable executable via PyInstaller (--onefile) for Linux, Windows, macOS
- Platform-native installation packages:
  - Linux: DEB, RPM, AppImage
  - Windows: Inno Setup EXE, MSI
  - macOS: PKG, DMG
- Cross-platform configuration with `platformdirs`:
  - Linux/macOS: `~/.config/netconnect/config.yaml`
  - Windows: `%APPDATA%\netconnect\config.yaml`
- Real socket-based connection testing:
  - TCP connection testing with latency measurement
  - UDP datagram testing
  - Port listeners with `select()` for TCP/UDP
- Modern CLI with subcommands:
  - `netconnect listen` - Create port listeners
  - `netconnect test` - Test connections to IP ranges
  - `netconnect config` - Manage configuration
- Multiple output formats: table, JSON, CSV
- Config file support for persistent defaults (duration, timeout, output format, protocol)
- Modern Python packaging with `pyproject.toml` (PEP 621)

### Changed
- Replaced 4 separate language implementations (Bash, Perl, Python, PowerShell) with single Python codebase
- Original scripts preserved as `.orig` backups
- Moved source to `src/netconnect/` with proper package structure
- IP range parsing now supports `start-end` format (e.g., `192.168.1.100-192.168.1.110`)

### Removed
- Interactive menu (not implemented in original Python version)
- Bash, Perl, PowerShell implementations (available as `.orig` backups)

## [1.1.0] - 2023-08-03

### Added
- Network hop checking in connection testing.
- Log network hops in case of failed connections.
- Automatic shutdown of created ports on exit.
- Duration option to keep the ports up for a specified time (default: 5 minutes).

## [1.0.0] - 2023-08-02

### Added
- Bash version of the NetConnect tool.
- Perl version of the NetConnect tool.
- Python version of the NetConnect tool.
- PowerShell version of the NetConnect tool.
- Interactive menu for user-friendly interactions.
- Command-line inputs for more flexibility.
- Support for creating multiple TCP/UDP ports on a server.
- Connectivity checking with other servers via multiple ports.
- Help option to display usage information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.