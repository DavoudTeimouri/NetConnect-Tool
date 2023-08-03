import subprocess

def test_port_connection(remote_server, *ports):
    for port in ports:
        print(f"Testing connectivity to {remote_server} on port {port}...")
        try:
            subprocess.run(["nc", "-z", "-w3", remote_server, str(port)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Connection to {remote_server} on port {port} succeeded.")
        except subprocess.CalledProcessError as e:
            print(f"Connection to {remote_server} on port {port} failed: {e.stderr.decode().strip()}")

def shutdown_ports(*ports):
    for port in ports:
        print(f"Shutting down port {port}...")
        # Stop-Process -Id (Get-NetTCPConnection -LocalPort $port).OwningProcess -Force
        # Uncomment the above line if you want to forcefully kill the process using the port

    print("All created ports have been shutdown.")

def show_menu(remote_server, *ports):
    print("========================")
    print("  NetConnect - Python Version")
    print("========================")
    print("1. Test Connectivity")
    print("2. Create Ports")
    print("3. Exit")
    print("========================")
    choice = input("Enter your choice: ")

    if choice == "1":
        test_port_connection(remote_server, *ports)
        show_menu(remote_server, *ports)
    elif choice == "2":
        ports_input = input("Enter the ports you want to create (space-separated): ")
        new_ports = [int(port) for port in ports_input.split()]
        for port in new_ports:
            print(f"Creating port {port}...")
            # Perform any specific actions needed for port creation
            # For demonstration purposes, we are not making any changes to the system.
        show_menu(remote_server, *(ports + new_ports))
    elif choice == "3":
        shutdown_ports(*ports)
        print("Exiting NetConnect...")
    else:
        print("Invalid choice. Please select a valid option.")
        show_menu(remote_server, *ports)

# Start the NetConnect tool
remote_server = input("Enter the remote server IP: ")
ports = []

show_menu(remote_server, *ports)
