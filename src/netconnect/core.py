"""Core connection testing logic for NetConnect."""

import socket
import ipaddress
import time
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    BOTH = "both"


@dataclass
class ConnectionResult:
    """Result of a connection test."""
    host: str
    port: int
    protocol: Protocol
    success: bool
    latency_ms: Optional[float] = None
    error: Optional[str] = None


@dataclass
class PortListener:
    """Represents a listening port."""
    port: int
    protocol: Protocol
    socket: Optional["socket.socket"] = None


def parse_ip_range(ip_range: str) -> List[str]:
    """Parse IP range string (e.g., '192.168.1.100-192.168.1.110') into list of IPs."""
    if '-' not in ip_range:
        return [ip_range]
    start_ip, end_ip = ip_range.split('-', 1)
    start = int(ipaddress.IPv4Address(start_ip.strip()))
    end = int(ipaddress.IPv4Address(end_ip.strip()))
    if start > end:
        start, end = end, start
    return [str(ipaddress.IPv4Address(i)) for i in range(start, end + 1)]


def test_tcp_connection(host: str, port: int, timeout: float = 5.0) -> ConnectionResult:
    """Test TCP connection to host:port."""
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            latency = (time.perf_counter() - start) * 1000
            return ConnectionResult(
                host=host,
                port=port,
                protocol=Protocol.TCP,
                success=True,
                latency_ms=latency
            )
    except socket.timeout:
        return ConnectionResult(
            host=host,
            port=port,
            protocol=Protocol.TCP,
            success=False,
            error=f"Timeout after {timeout}s"
        )
    except ConnectionRefusedError:
        return ConnectionResult(
            host=host,
            port=port,
            protocol=Protocol.TCP,
            success=False,
            error="Connection refused"
        )
    except OSError as e:
        return ConnectionResult(
            host=host,
            port=port,
            protocol=Protocol.TCP,
            success=False,
            error=str(e)
        )


def test_udp_connection(host: str, port: int, timeout: float = 5.0) -> ConnectionResult:
    """Test UDP connection to host:port (sends empty datagram)."""
    start = time.perf_counter()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        # UDP is connectionless - send empty packet and see if we get ICMP error
        sock.sendto(b'', (host, port))
        # Try to receive response (will timeout if nothing)
        try:
            sock.recvfrom(1024)
        except socket.timeout:
            pass
        latency = (time.perf_counter() - start) * 1000
        sock.close()
        return ConnectionResult(
            host=host,
            port=port,
            protocol=Protocol.UDP,
            success=True,
            latency_ms=latency
        )
    except OSError as e:
        return ConnectionResult(
            host=host,
            port=port,
            protocol=Protocol.UDP,
            success=False,
            error=str(e)
        )


def test_connection(host: str, port: int, protocol: Protocol, timeout: float = 5.0) -> List[ConnectionResult]:
    """Test connection with specified protocol."""
    results = []
    if protocol in (Protocol.TCP, Protocol.BOTH):
        results.append(test_tcp_connection(host, port, timeout))
    if protocol in (Protocol.UDP, Protocol.BOTH):
        results.append(test_udp_connection(host, port, timeout))
    return results


def create_tcp_listener(port: int, host: str = '0.0.0.0') -> Optional[socket.socket]:
    """Create a TCP listener on specified port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        return sock
    except OSError:
        return None


def create_udp_listener(port: int, host: str = '0.0.0.0') -> Optional[socket.socket]:
    """Create a UDP listener on specified port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        return sock
    except OSError:
        return None


def create_listeners(ports: List[int], protocol: Protocol = Protocol.BOTH) -> List[PortListener]:
    """Create listeners on specified ports."""
    listeners = []
    for port in ports:
        if protocol in (Protocol.TCP, Protocol.BOTH):
            sock = create_tcp_listener(port)
            if sock:
                listeners.append(PortListener(port=port, protocol=Protocol.TCP, socket=sock))
        if protocol in (Protocol.UDP, Protocol.BOTH):
            sock = create_udp_listener(port)
            if sock:
                listeners.append(PortListener(port=port, protocol=Protocol.UDP, socket=sock))
    return listeners


def close_listeners(listeners: List[PortListener]) -> None:
    """Close all listener sockets."""
    for listener in listeners:
        if listener.socket:
            try:
                listener.socket.close()
            except OSError:
                pass


def run_listeners(listeners: List[PortListener], duration: Optional[int] = None) -> None:
    """Run listeners for specified duration (seconds) or indefinitely."""
    import select
    import sys
    
    sockets = [l.socket for l in listeners if l.socket]
    if not sockets:
        print("No listeners created")
        return
    
    print(f"Listening on {len(sockets)} socket(s)... Press Ctrl+C to stop")
    if duration:
        print(f"Will stop after {duration} seconds")
    
    start_time = time.time()
    try:
        while True:
            if duration and (time.time() - start_time) >= duration:
                print(f"\nDuration {duration}s reached, stopping...")
                break
            
            # Use select to wait for connections with timeout
            ready, _, _ = select.select(sockets, [], [], 1.0)
            for sock in ready:
                try:
                    if sock.type == socket.SOCK_STREAM:
                        conn, addr = sock.accept()
                        print(f"TCP connection from {addr[0]}:{addr[1]} on port {sock.getsockname()[1]}")
                        conn.close()
                    else:
                        data, addr = sock.recvfrom(1024)
                        print(f"UDP packet from {addr[0]}:{addr[1]} on port {sock.getsockname()[1]} ({len(data)} bytes)")
                except OSError:
                    pass
    except KeyboardInterrupt:
        print("\nStopped by user")