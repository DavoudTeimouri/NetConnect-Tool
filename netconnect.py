#!/usr/bin/env python3

import sys
import socket
import subprocess

# Function to create TCP/UDP ports on the server
def create_ports(ports):
    for port in ports:
        subprocess.Popen(['nc', '-l', '-p', str(port)])
        subprocess.Popen(['nc', '-ul', '-p', str(port)])

# Function to check connectivity with multiple servers via multiple ports
def check_connectivity(servers, ports):
    for server in servers:
        for port in ports:
            print(f"Checking connectivity to {server} on port {port}...")
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((server, port))
                    print(f"Connected to {server} on port {port}")
            except Exception as e:
                print(f"Connection to {server} on port {port} failed: {e}")

# Main menu function
def main_menu():
    print("==== TCP/UDP Connection Tool ====")
    print("1. Create TCP/UDP Ports")
    print("2. Check Connectivity with Other Servers")
    print("3. Exit")
    print("=================================")

    choice = input().strip()

    if choice == '1':
        ports_input = input("Enter the ports to create (separated by spaces, e.g., '8080 8888 9000'): ")
        ports = [int(port) for port in ports_input.split()]
        create_ports(ports)
    elif choice == '2':
        servers_input = input("Enter the servers or IP addresses to check (separated by spaces, e.g., '192.168.1.100 192.168.1.200 10.0.0.1-10.0.0.10'): ")
        servers = servers_input.split()
        ports_input = input("Enter the ports to check (separated by spaces, e.g., '80 443 8080'): ")
        ports = [int(port) for port in ports_input.split()]
        check_connectivity(servers, ports)
    elif choice == '3':
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")

    main_menu()

# Start the script by displaying the main menu
main_menu()
