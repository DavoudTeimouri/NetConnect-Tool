package NetConnect;

use strict;
use warnings;

sub test_port_connection {
    my ($remote_server, @ports) = @_;

    foreach my $port (@ports) {
        print "Testing connectivity to $remote_server on port $port...\n";
        my $result = `nc -z -w3 $remote_server $port 2>&1`;
        if ($? == 0) {
            print "Connection to $remote_server on port $port succeeded.\n";
        } else {
            print "Connection to $remote_server on port $port failed: $result\n";
        }
    }
}

sub shutdown_ports {
    my @ports = @_;

    foreach my $port (@ports) {
        print "Shutting down port $port...\n";
        # Stop-Process -Id (Get-NetTCPConnection -LocalPort $port).OwningProcess -Force
        # Uncomment the above line if you want to forcefully kill the process using the port
    }

    print "All created ports have been shutdown.\n";
}

sub show_menu {
    my ($remote_server, @ports) = @_;

    print "========================\n";
    print "  NetConnect - Perl Version\n";
    print "========================\n";
    print "1. Test Connectivity\n";
    print "2. Create Ports\n";
    print "3. Exit\n";
    print "========================\n";
    print "Enter your choice: ";
    my $choice = <>;
    chomp($choice);

    if ($choice eq "1") {
        test_port_connection($remote_server, @ports);
        show_menu($remote_server, @ports);
    } elsif ($choice eq "2") {
        print "Enter the ports you want to create (space-separated): ";
        my $ports_input = <>;
        chomp($ports_input);
        my @new_ports = split(' ', $ports_input);
        foreach my $port (@new_ports) {
            print "Creating port $port...\n";
            # Perform any specific actions needed for port creation
            # For demonstration purposes, we are not making any changes to the system.
        }
        show_menu($remote_server, (@ports, @new_ports));
    } elsif ($choice eq "3") {
        shutdown_ports(@ports);
        print "Exiting NetConnect...\n";
    } else {
        print "Invalid choice. Please select a valid option.\n";
        show_menu($remote_server, @ports);
    }
}

# Start the NetConnect tool
print "Enter the remote server IP: ";
my $remote_server = <>;
chomp($remote_server);
my @ports = ();

show_menu($remote_server, @ports);

1;
