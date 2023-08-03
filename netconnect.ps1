function Test-PortConnection {
    param (
        [string]$RemoteServer,
        [int[]]$Ports
    )
    foreach ($Port in $Ports) {
        $result = Test-NetConnection -ComputerName $RemoteServer -Port $Port -TraceRoute
        Write-Output "Testing connectivity to $RemoteServer on port $Port..."
        if ($result.TcpTestSucceeded) {
            Write-Output "Connection to $RemoteServer on port $Port succeeded."
        } else {
            Write-Output "Connection to $RemoteServer on port $Port failed."
        }
        if ($result.Hops -ne $null) {
            Write-Output "Network Hops:"
            foreach ($hop in $result.Hops) {
                Write-Output "$($hop.HopNumber). $($hop.Address) - $($hop.ResponseTime)ms"
            }
        }
    }
}

function Shutdown-Ports {
    param (
        [int[]]$Ports
    )
    foreach ($Port in $Ports) {
        Write-Output "Shutting down port $Port..."
        # Stop-Process -Id (Get-NetTCPConnection -LocalPort $Port).OwningProcess -Force
        # Uncomment the above line if you want to forcefully kill the process using the port
    }
    Write-Output "All created ports have been shutdown."
}

function Show-Menu {
    param (
        [string]$RemoteServer,
        [int[]]$Ports
    )
    Write-Output "========================"
    Write-Output "  NetConnect - PowerShell Version"
    Write-Output "========================"
    Write-Output "1. Test Connectivity"
    Write-Output "2. Create Ports"
    Write-Output "3. Exit"
    Write-Output "========================"
    $choice = Read-Host "Enter your choice: "

    switch ($choice) {
        1 {
            Test-PortConnection -RemoteServer $RemoteServer -Ports $Ports
            Show-Menu -RemoteServer $RemoteServer -Ports $Ports
        }
        2 {
            $portsInput = Read-Host "Enter the ports you want to create (comma-separated): "
            $newPorts = $portsInput -split ',' | ForEach-Object { $_.Trim() -as [int] }
            $duration = Read-Host "Enter the duration in seconds to keep the ports up (press Enter for default 5 minutes): "
            if ([string]::IsNullOrEmpty($duration)) {
                $duration = 300  # Default: 5 minutes (300 seconds)
            } else {
                $duration = [int]$duration
            }

            foreach ($port in $newPorts) {
                Write-Output "Creating port $port..."
                # Perform any specific actions needed for port creation
                # For demonstration purposes, we are not making any changes to the system.
            }
            
            Start-Sleep -Seconds $duration
            Shutdown-Ports -Ports $newPorts
            Show-Menu -RemoteServer $RemoteServer -Ports $Ports
        }
        3 {
            if ($Ports.Count -gt 0) {
                Shutdown-Ports -Ports $Ports
            }
            Write-Output "Exiting NetConnect..."
        }
        default {
            Write-Output "Invalid choice. Please select a valid option."
            Show-Menu -RemoteServer $RemoteServer -Ports $Ports
        }
    }
}

# Start the NetConnect tool
$RemoteServer = Read-Host "Enter the remote server IP: "
$Ports = @()

Show-Menu -RemoteServer $RemoteServer -Ports $Ports
