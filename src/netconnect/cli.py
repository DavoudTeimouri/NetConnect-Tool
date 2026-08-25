"""CLI entry point for NetConnect."""

import sys
import argparse
import json
import csv
from typing import List, Optional
from tabulate import tabulate

from netconnect.core import (
    parse_ip_range,
    test_connection,
    create_listeners,
    close_listeners,
    run_listeners,
    Protocol,
    ConnectionResult,
)
from netconnect.config import config_manager, NetConnectConfig
from netconnect import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="netconnect",
        description="NetConnect - Cross-platform TCP/UDP Connection Testing Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create TCP/UDP listeners on ports 8080, 9000
  netconnect listen -p 8080 9000 --duration 60
  
  # Test TCP connections to ports 22, 80, 443 on IP range
  netconnect test -t 192.168.1.100-192.168.1.110 -p 22 80 443
  
  # Test with UDP only, JSON output
  netconnect test -t 10.0.0.1-10.0.0.10 -p 53 --protocol udp --output json
  
  # Show config file location
  netconnect config --show-path
        """
    )
    
    # Global options
    parser.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="Increase verbosity (use -vv for debug)"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--config", help="Path to config file (overrides default)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # listen command
    listen_parser = subparsers.add_parser("listen", help="Create port listeners")
    listen_parser.add_argument(
        "-p", "--ports", nargs="+", type=int, required=True,
        help="Ports to listen on"
    )
    listen_parser.add_argument(
        "--protocol", choices=["tcp", "udp", "both"], default="both",
        help="Protocol to listen on (default: both)"
    )
    listen_parser.add_argument(
        "--duration", type=int,
        help="Duration in seconds to keep listeners running"
    )
    listen_parser.add_argument(
        "--host", default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    
    # test command
    test_parser = subparsers.add_parser("test", help="Test connections")
    test_parser.add_argument(
        "-t", "--targets", required=True,
        help="Target IP range (e.g., 192.168.1.100-192.168.1.110) or single IP"
    )
    test_parser.add_argument(
        "-p", "--ports", nargs="+", type=int, required=True,
        help="Ports to test"
    )
    test_parser.add_argument(
        "--protocol", choices=["tcp", "udp", "both"], default="both",
        help="Protocol to test (default: both)"
    )
    test_parser.add_argument(
        "--timeout", type=float,
        help="Connection timeout in seconds"
    )
    test_parser.add_argument(
        "--output", choices=["table", "json", "csv"], default="table",
        help="Output format (default: table)"
    )
    
    # config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_sub = config_parser.add_subparsers(dest="config_action")
    config_sub.add_parser("show", help="Show current configuration")
    config_sub.add_parser("show-path", help="Show config file path")
    config_sub.add_parser("reset", help="Reset to defaults")
    set_parser = config_sub.add_parser("set", help="Set config value")
    set_parser.add_argument("key", help="Config key (e.g., defaults.duration)")
    set_parser.add_argument("value", help="Config value")
    
    return parser


def output_results(results: List[ConnectionResult], format_type: str) -> None:
    """Output connection results in specified format."""
    if format_type == "json":
        data = [
            {
                "host": r.host,
                "port": r.port,
                "protocol": r.protocol.value,
                "success": r.success,
                "latency_ms": round(r.latency_ms, 2) if r.latency_ms else None,
                "error": r.error
            }
            for r in results
        ]
        print(json.dumps(data, indent=2))
    
    elif format_type == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(["host", "port", "protocol", "success", "latency_ms", "error"])
        for r in results:
            writer.writerow([
                r.host, r.port, r.protocol.value,
                r.success, round(r.latency_ms, 2) if r.latency_ms else "",
                r.error or ""
            ])
    
    else:  # table
        headers = ["Host", "Port", "Protocol", "Status", "Latency (ms)", "Error"]
        rows = []
        for r in results:
            status = "OPEN" if r.success else "CLOSED"
            latency = f"{r.latency_ms:.2f}" if r.latency_ms else "N/A"
            error = r.error or ""
            rows.append([r.host, r.port, r.protocol.value.upper(), status, latency, error])
        print(tabulate(rows, headers=headers, tablefmt="grid"))


def cmd_listen(args) -> int:
    """Handle listen command."""
    protocol_map = {"tcp": Protocol.TCP, "udp": Protocol.UDP, "both": Protocol.BOTH}
    protocol = protocol_map[args.protocol]
    
    print(f"Creating listeners on ports: {args.ports} ({args.protocol.upper()})")
    
    listeners = create_listeners(args.ports, protocol)
    if not listeners:
        print("Error: Failed to create any listeners", file=sys.stderr)
        return 1
    
    try:
        run_listeners(listeners, args.duration)
    finally:
        close_listeners(listeners)
    
    return 0


def cmd_test(args) -> int:
    """Handle test command."""
    config = config_manager.load()
    defaults = config.defaults
    
    timeout = args.timeout or defaults.get("timeout", 5.0)
    output_format = args.output or defaults.get("output", "table")
    protocol_map = {"tcp": Protocol.TCP, "udp": Protocol.UDP, "both": Protocol.BOTH}
    protocol = protocol_map[args.protocol or defaults.get("protocol", "both")]
    
    hosts = parse_ip_range(args.targets)
    print(f"Testing {len(hosts)} host(s) on {len(args.ports)} port(s) ({args.protocol.upper()})...")
    
    all_results = []
    for host in hosts:
        for port in args.ports:
            results = test_connection(host, port, protocol, timeout)
            all_results.extend(results)
    
    output_results(all_results, output_format)
    
    # Return non-zero if any failed
    failed = sum(1 for r in all_results if not r.success)
    return 1 if failed > 0 else 0


def cmd_config(args) -> int:
    """Handle config command."""
    config = config_manager.load()
    
    if args.config_action == "show":
        print(f"Config file: {config_manager.get_config_path()}")
        print("Current configuration:")
        print(f"  defaults: {config.defaults}")
        print(f"  logging: {config.logging}")
    
    elif args.config_action == "show-path":
        print(config_manager.get_config_path())
    
    elif args.config_action == "reset":
        config_manager.save(NetConnectConfig())
        print("Configuration reset to defaults")
    
    elif args.config_action == "set":
        # Handle nested keys like defaults.duration
        if args.key.startswith("defaults."):
            key = args.key[9:]  # remove "defaults."
            try:
                # Try to convert to appropriate type
                if args.value.lower() in ("true", "false"):
                    value = args.value.lower() == "true"
                elif args.value.isdigit():
                    value = int(args.value)
                else:
                    try:
                        value = float(args.value)
                    except ValueError:
                        value = args.value
                config_manager.set_default(key, value)
                print(f"Set defaults.{key} = {value}")
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                return 1
        else:
            print(f"Error: Unknown config key: {args.key}", file=sys.stderr)
            return 1
    
    else:
        print("Error: No config action specified", file=sys.stderr)
        return 1
    
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Set verbosity
    if args.verbose >= 2:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose >= 1:
        import logging
        logging.basicConfig(level=logging.INFO)
    
    # Load custom config if provided
    if args.config:
        # For simplicity, we'll just note this - full implementation would merge
        pass
    
    try:
        if args.command == "listen":
            return cmd_listen(args)
        elif args.command == "test":
            return cmd_test(args)
        elif args.command == "config":
            return cmd_config(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose >= 2:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())