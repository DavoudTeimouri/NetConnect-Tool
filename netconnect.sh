#!/bin/bash

usage() {
    echo "NetConnect - TCP/UDP Connection Testing Tool"
    echo
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -h, --help            Show this help message and exit."
    echo "  -c PORT_1 PORT_2 ...  Create TCP/UDP ports on the local computer."
    echo "  -t SERVER_RANGE       Test connections with multiple servers or a range of IP addresses."
    echo "  -p PORT_1 PORT_2 ...  Ports to test connections with."
    echo
    echo "Examples:"
    echo "  Create ports 8080 and 9000 on the local computer:"
    echo "  $0 -c 8080 9000"
    echo
    echo "  Test connectivity to ports 22, 80, and 443 on multiple servers:"
    echo "  $0 -t 192.168.1.100-203.0.113.10 -p 22 80 443"
}

create_ports() {
    echo "Creating TCP/UDP ports on the local computer..."
    # Implement the logic to create ports here
    for port in "$@"; do
        echo "Port $port created."
    done
}

test_connections() {
    echo "Testing connections..."
    # Implement the logic to test connections here
    for server in "${servers[@]}"; do
        for port in "${ports[@]}"; do
            echo "Testing connectivity to $server:$port ..."
            # Implement the logic to test connection to each server and port here
            # Output success or failure messages accordingly
        done
    done
}

# Parse command-line options
while getopts "hc:t:p:" opt; do
    case "$opt" in
    h)
        usage
        exit 0
        ;;
    c)
        create_ports "$@"
        exit 0
        ;;
    t)
        server_range=$OPTARG
        ;;
    p)
        ports=($OPTARG)
        ;;
    esac
done

# Check if both create and test options are used together
if [ -n "$server_range" ] && [ ${#ports[@]} -gt 0 ]; then
    echo "Error: Cannot use create ports and test options together."
    echo
    usage
    exit 1
fi

# Check if either create or test options are used
if [ -z "$server_range" ] && [ ${#ports[@]} -eq 0 ]; then
    # No options provided, run the interactive menu
    echo "Interactive menu is not yet implemented. Use command-line options instead."
    exit 1
fi

# Check if test option is used without specifying ports
if [ -n "$server_range" ] && [ ${#ports[@]} -eq 0 ]; then
    echo "Error: Test option requires specifying ports with the -p option."
    echo
    usage
    exit 1
fi

# Check if test option is used without specifying servers
if [ -z "$server_range" ] && [ ${#ports[@]} -gt 0 ]; then
    echo "Error: Test option requires specifying servers with the -t option."
    echo
    usage
    exit 1
fi

# Split server_range into start and end IPs
IFS='-' read -ra ADDR <<<"$server_range"
start_ip=${ADDR[0]}
end_ip=${ADDR[1]}

# Generate the array of servers from the range
mapfile -t servers < <(python3 -c "import ipaddress; [print(ip) for ip in ipaddress.summarize_address_range(ipaddress.IPv4Address('$start_ip'), ipaddress.IPv4Address('$end_ip'))]")

# Perform the test connections
test_connections
