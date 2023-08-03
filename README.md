# NetConnect - TCP/UDP Connection Testing Tool

NetConnect is a simple command-line tool that allows you to create TCP/UDP ports on a server and check connectivity with other servers via multiple ports. It provides both interactive menu-driven interactions and support for command-line inputs.

## Features

- Create TCP/UDP ports on a server.
- Check connectivity with other servers via multiple ports.
- Supports both interactive menu-driven interactions and command-line inputs.
- Includes a help option to display usage information.
- Network hop checking to trace the route of failed connections.
- Automatic shutdown of created ports on exit.
- Duration option to keep the ports up for a specified time (default: 5 minutes).

## Requirements

- For Bash version: Linux/Unix-based system.
- For Perl version: Perl interpreter.
- For Python version: Python 3.
- For PowerShell version: Windows OS (PowerShell is built into Windows and does not have any additional dependencies).

## Usage

### Bash Version

`./netconnect.sh`

### Perl Version

`perl netconnect.pl`

### Python Version

`python3 netconnect.py`

### PowerShell Version

`.\netconnect.ps1`

## Command-Line Options

Each version of the NetConnect tool supports command-line options to create ports and test connections separately. If no duration is provided, the default duration is 5 minutes (300 seconds).

### Bash

#### To create ports on the local computer
`./netconnect.sh -c <PORT_1> <PORT_2> ...`

#### To test connections with multiple servers or a range of IP addresses and ports from the local computer
`./netconnect.sh -t <REMOTE_SERVER1-REMOTE_SERVER2> -p <PORT_1> <PORT_2> ...`

### Perl

#### To create ports on the local computer
`perl netconnect.pl -c <PORT_1> <PORT_2> ...`

#### To test connections with multiple servers or a range of IP addresses and ports from the local computer
`perl netconnect.pl -t <REMOTE_SERVER1-REMOTE_SERVER2> -p <PORT_1> <PORT_2> ...`

### Python

#### To create ports on the local computer
`python3 netconnect.py -c <PORT_1> <PORT_2> ...`

#### To test connections with multiple servers or a range of IP addresses and ports from the local computer
`python3 netconnect.py -t <REMOTE_SERVER1-REMOTE_SERVER2> -p <PORT_1> <PORT_2> ...`

### PowerShell

#### To create ports on the local computer
`.\netconnect.ps1 -c <PORT_1> <PORT_2> ...`

#### To test connections with multiple servers or a range of IP addresses and ports from the local computer
`.\netconnect.ps1 -t <REMOTE_SERVER1-REMOTE_SERVER2> -p <PORT_1>,<PORT_2>,...`

### Examples

1. Create ports 8080 and 9000 on the local computer using PowerShell:

`.\netconnect.ps1 -c 8080 9000`

2. Test connectivity to ports 22, 80, and 443 on multiple servers (192.168.1.100, 203.0.113.10) using Bash:

`./netconnect.sh -t 192.168.1.100-203.0.113.10 -p 22 80 443`

3. Test connectivity to ports 80 and 443 on a range of IP addresses (192.168.1.100-192.168.1.110) using Python:

`python3 netconnect.py -t 192.168.1.100-192.168.1.110 -p 80 443`

## Help Option

To display usage information and help, use the `-h` or `--help` option with any version of the script:

`./netconnect.sh -h`

`perl netconnect.pl -h`

`python3 netconnect.py -h`

`.\netconnect.ps1 -h`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
