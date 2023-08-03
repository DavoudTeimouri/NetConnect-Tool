# NetConnect - TCP/UDP Connection Testing Tool

NetConnect is a simple command-line tool that allows you to create TCP/UDP ports on a server and check connectivity with other servers via multiple ports. It provides both interactive menu-driven interactions and support for command-line inputs.

## Features

- Create TCP/UDP ports on a server.
- Check connectivity with other servers via multiple ports.
- Supports both interactive menu-driven interactions and command-line inputs.
- Includes a help option to display usage information.

## Requirements

- For Bash version: Linux/Unix-based system.
- For Perl version: Perl interpreter.
- For Python version: Python 3.
- For PowerShell version: Windows OS.

## Usage

### Bash Version

Run the script with the following options:

1. To create multiple ports: `./netconnect.sh -c <port1> [<port2> ...]`
   Example: `./netconnect.sh -c 8080 8888 9000`

2. To check connectivity with other servers: `./netconnect.sh -ch -s <IP> -p <port>`
   Example: `./netconnect.sh -ch -s 192.168.1.100 -p 80`

3. To use the interactive menu: `./netconnect.sh`

### Perl Version

Run the script with the following options:

1. To create multiple ports: `perl netconnect.pl -c <port1> [<port2> ...]`
   Example: `perl netconnect.pl -c 8080 8888 9000`

2. To check connectivity with other servers: `perl netconnect.pl -ch -s <IP> -p <port>`
   Example: `perl netconnect.pl -ch -s 192.168.1.100 -p 80`

3. To use the interactive menu: `perl netconnect.pl`

### Python Version

Run the script with the following options:

1. To create multiple ports: `python3 netconnect.py -c <port1> [<port2> ...]`
   Example: `python3 netconnect.py -c 8080 8888 9000`

2. To check connectivity with other servers: `python3 netconnect.py -ch -s <IP> -p <port>`
   Example: `python3 netconnect.py -ch -s 192.168.1.100 -p 80`

3. To use the interactive menu: `python3 netconnect.py`

### PowerShell Version

Run the script with the following options:

1. To create multiple ports: `.\netconnect.ps1 -c <port1> [<port2> ...]`
   Example: `.\netconnect.ps1 -c 8080 8888 9000`

2. To check connectivity with other servers: `.\netconnect.ps1 -ch -s <IP> -p <port>`
   Example: `.\netconnect.ps1 -ch -s 192.168.1.100 -p 80`

3. To use the interactive menu: `.\netconnect.ps1`

### Help Option

To display usage information and help, use the `-h` or `--help` option with any version of the script:

`./netconnect.sh -h`

`perl netconnect.pl -h`

`python3 netconnect.py -h`

`.\netconnect.ps1 -h`
