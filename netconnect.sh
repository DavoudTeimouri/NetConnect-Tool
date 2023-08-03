#!/bin/bash

function test_port_connection {
    remote_server=$1
    ports=("${@:2}")

    for port in "${ports[@]}"; do
        echo "Testing connectivity to $remote_server on port $port..."
        nc -z -w3 "$remote_server" "$port"
        if [ $? -eq 0 ]; then
            echo "Connection to $remote_server on port $port succeeded."
        else
            echo "Connection to $remote_server on port $port failed."
        fi
    done
}

function shutdown_ports {
    ports=("${@}")

    for port in "${ports[@]}"; do
        echo "Shutting down port $port..."
        # Stop-Process -Id (Get-NetTCPConnection -LocalPort $port).OwningProcess -Force
        # Uncomment the above line if you want to forcefully kill the process using the port
    done

    echo "All created ports have been shutdown."
}

function show_menu {
    remote_server=$1
    ports=("${@:2}")

    echo "========================"
    echo "  NetConnect - Bash Version"
    echo "========================"
    echo "1. Test Connectivity"
    echo "2. Create Ports"
    echo "3. Exit"
    echo "========================"
    read -p "Enter your choice: " choice

    case $choice in
        1)
            test_port_connection "$remote_server" "${ports[@]}"
            show_menu "$remote_server" "${ports[@]}"
            ;;
        2)
            echo "Enter the ports you want to create (comma-separated): "
            read ports_input
            new_ports=($(echo "$ports_input" | tr ',' '\n'))
            for port in "${new_ports[@]}"; do
                echo "Creating port $port..."
                # Perform any specific actions needed for port creation
                # For demonstration purposes, we are not making any changes to the system.
            done
            show_menu "$remote_server" "${ports[@]}" "${new_ports[@]}"
            ;;
        3)
            shutdown_ports "${ports[@]}"
            echo "Exiting NetConnect..."
            ;;
        *)
            echo "Invalid choice. Please select a valid option."
            show_menu "$remote_server" "${ports[@]}"
            ;;
    esac
}

# Start the NetConnect tool
echo "Enter the remote server IP: "
read remote_server
ports=()

show_menu "$remote_server" "${ports[@]}"
