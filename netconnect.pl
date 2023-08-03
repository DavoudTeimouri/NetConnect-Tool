#!/usr/bin/perl

use strict;
use warnings;
use Net::Ping;

# Function to create TCP/UDP ports on the server
sub create_ports {
    my @ports = @_;
    foreach my $port (@ports) {
        system("nc -l -p $port &");
        system("nc -ul -p $port &");
    }
}

# Function to check connectivity with multiple servers via multiple ports
sub check_connectivity {
    my (@servers, @ports) = @_;

    foreach my $server (@servers) {
        foreach my $port (@ports) {
            print "Checking connectivity to $server on port $port...\n";
            my $p = Net::Ping->new();
            if ($p->ping($server)) {
                print "Ping successful.\n";
                my $result = `nc -zv $server $port 2>&1`;
                print "$result\n";
            } else {
                print "Ping failed.\n";
            }
        }
    }
}

# Main menu function
sub main_menu {
    print "==== TCP/UDP Connection Tool ====\n";
    print "1. Create TCP/UDP Ports\n";
    print "2. Check Connectivity with Other Servers\n";
    print "3. Exit\n";
    print "================================\n";

    my $choice = <STDIN>;
    chomp($choice);

    given ($choice) {
        when (1) {
            print "Enter the ports to create (separated by spaces, e.g., '8080 8888 9000'): ";
            my $ports_input = <STDIN>;
            chomp($ports_input);
            my @ports = split(/\s+/, $ports_input);
            create_ports(@ports);
        }
        when (2) {
            print "Enter the servers or IP addresses to check (separated by spaces, e.g., '192.168.1.100 192.168.1.200 10.0.0.1-10.0.0.10'): ";
            my $servers_input = <STDIN>;
            chomp($servers_input);
            my @servers = split(/\s+/, $servers_input);

            print "Enter the ports to check (separated by spaces, e.g., '80 443 8080'): ";
            my $ports_input = <STDIN>;
            chomp($ports_input);
            my @ports = split(/\s+/, $ports_input);

            check_connectivity(@servers, @ports);
        }
        when (3) {
            print "Exiting...\n";
            exit 0;
        }
        default {
            print "Invalid choice. Please try again.\n";
        }
    }

    main_menu();
}

# Start the script by displaying the main menu
main_menu();
