#!/usr/bin/env python3

import argparse
import ipaddress

def usage():
    print('''NetConnect - TCP/UDP Connection Testing Tool

Usage: netconnect.py [options]

Options:
  -h, --help            Show this help message and exit.
  -c PORT_1 PORT_2 ...  Create TCP/UDP ports on the local computer.
  -t SERVER_RANGE       Test connections with multiple servers or a range of IP addresses.
  -p PORT_1 PORT_2 ...  Ports to test connections with.

Examples:
  Create ports 8080 and 9000 on the local computer:
  netconnect.py -c 8080 9000

  Test connectivity to ports 22, 80, and 443 on multiple servers:
  netconnect.py -t 192.168.1.100-203.0.113.10 -p 22 80 443
''')

def create_ports(*ports):
    print("Creating TCP/UDP ports on the local computer...")
    # Implement the logic to create ports here
    for port in ports:
        print(f"Port {port} created.")

def test_connections(servers, ports):
    print("Testing connections...")
    # Implement the logic to test connections here
    for server in servers:
        for port in ports:
            print(f"Testing connectivity to {server}:{port} ...")
            # Implement the logic to test connection to each server and port here
            # Output success or failure messages accordingly

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NetConnect - TCP/UDP Connection Testing Tool")
    parser.add_argument('-c', nargs='+', type=int, help='Create TCP/UDP ports on the local computer.')
    parser.add_argument('-t', metavar='SERVER_RANGE', help='Test connections with multiple servers or a range of IP addresses.')
    parser.add_argument('-p', nargs='+', type=int, help='Ports to test connections with.')

    args = parser.parse_args()

    # Check if both create and test options are used together
    if args.c and args.t:
        print("Error: Cannot use create ports and test options together.")
        usage()
        exit(1)

    # Check if either create or test options are used
    if not args.c and not args.t:
        # No options provided, run the interactive menu
        print("Interactive menu is not yet implemented. Use command-line options instead.")
        exit(1)

    # Check if test option is used without specifying ports
    if args.t and not args.p:
        print("Error: Test option requires specifying ports with the -p option.")
        usage()
        exit(1)

    # Check if test option is used without specifying servers
    if not args.t and args.p:
        print("Error: Test option requires specifying servers with the -t option.")
        usage()
        exit(1)

    if args.c:
        create_ports(*args.c)
    elif args.t and args.p:
        # Split server_range into start and end IPs
        start_ip, end_ip = args.t.split('-')
        servers = [str(ip) for ip in ipaddress.summarize_address_range(ipaddress.IPv4Address(start_ip), ipaddress.IPv4Address(end_ip))]
        test_connections(servers, args.p)
