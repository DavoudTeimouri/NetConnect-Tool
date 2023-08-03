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

Each version of the NetConnect tool supports command-line options to create ports and specify the duration to keep the ports up. If no duration is provided, the default duration is 5 minutes (300 seconds).

### Bash

`./netconnect.sh -c <port1> [<port2> ...] -d <duration_in_seconds>`

### Perl

`perl netconnect.pl -c <port1> [<port2> ...] -d <duration_in_seconds>`

### Python

`python3 netconnect.py -c <port1> [<port2> ...] -d <duration_in_seconds>`

### PowerShell

`.\netconnect.ps1 -c <port1> [<port2> ...] -d <duration_in_seconds>`

### Examples

1. Create ports 8080 and 9000 on remote server 192.168.1.100 using PowerShell and keep them up for 10 minutes:

`.\netconnect.ps1 -c 192.168.1.100 8080,9000 -d 600`

2. Test connectivity to ports 22, 80, and 443 on remote server example.com using Python:

`python3 netconnect.py -c example.com 22 80 443`

## Help Option

To display usage information and help, use the `-h` or `--help` option with any version of the script:

`./netconnect.sh -h`

`perl netconnect.pl -h`

`python3 netconnect.py -h`

`.\netconnect.ps1 -h`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Please copy the updated content and paste it into the README.md file in your project repository. The updated README.md now includes information about the new features, command-line options, examples, and the help option.
