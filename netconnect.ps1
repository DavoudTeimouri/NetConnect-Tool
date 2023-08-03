# Function to create TCP/UDP ports on the server
function Create-Ports {
    param (
        [int[]]$Ports
    )

    foreach ($port in $Ports) {
        Start-Process -NoNewWindow "nc.exe" "-l -p $port"
        Start-Process -NoNewWindow "nc.exe" "-ul -p $port"
    }
}

# Function to check connectivity with multiple servers via multiple ports
function Check-Connectivity {
    param (
        [string[]]$Servers,
        [int[]]$Ports
    )

    foreach ($server in $Servers) {
        foreach ($port in $Ports) {
            Write-Host "Checking connectivity to $server on port $port..."
            try {
                $socket = New-Object System.Net.Sockets.TcpClient
                $socket.Connect($server, $port)
                $socket.Close()
                Write-Host "Connected to $server on port $port"
            }
            catch {
                Write-Host "Connection to $server on port $port failed: $($_.Exception.Message)"
            }
        }
    }
}

# Main menu function
function Show-MainMenu {
    Write-Host "==== TCP/UDP Connection Tool ===="
    Write-Host "1. Create TCP/UDP Ports"
    Write-Host "2. Check Connectivity with Other Servers"
    Write-Host "3. Exit"
    Write-Host "================================"

    $choice = Read-Host

    switch ($choice) {
        1 {
            $ports_input = Read-Host "Enter the ports to create (separated by spaces, e.g., '8080 8888 9000'): "
            $ports = $ports_input -split '\s' | ForEach-Object { [int]$_ }
            Create-Ports -Ports $ports
        }
        2 {
            $servers_input = Read-Host "Enter the servers or IP addresses to check (separated by spaces, e.g., '192.168.1.100 192.168.1.200 10.0.0.1-10.0.0.10'): "
            $servers = $servers_input -split '\s'
            $ports_input = Read-Host "Enter the ports to check (separated by spaces, e.g., '80 443 8080'): "
            $ports = $ports_input -split '\s' | ForEach-Object { [int]$_ }
            Check-Connectivity -Servers $servers -Ports $ports
        }
        3 {
            Write-Host "Exiting..."
            exit 0
        }
        default {
            Write-Host "Invalid choice. Please try again."
        }
    }

    Show-MainMenu
}

# Start the script by displaying the main menu
Show-MainMenu
