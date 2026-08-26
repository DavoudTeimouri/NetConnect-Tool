"""Core connection testing logic for NetConnect."""

import socket
import ipaddress
import time
import ssl
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
    ssl_context: Optional["ssl.SSLContext"] = None


# Banner sent to clients (curl, telnet, nc, ...) on a successful TCP connection.
APP_BANNER = "NetConnect"
APP_VERSION = "2.1.1"


def banner_text() -> str:
    """Build the identification banner sent to connecting clients."""
    return f"{APP_BANNER}/{APP_VERSION} (NetConnect cross-platform connectivity tool)\r\n"


def build_ssl_context(certfile: Optional[str] = None, keyfile: Optional[str] = None) -> ssl.SSLContext:
    """Create a TLS context for the listener.

    If ``certfile`` is supplied it (and optionally ``keyfile``) is loaded.
    Otherwise a self-signed certificate is generated on the fly via the
    system ``openssl`` binary (present on Linux/macOS and most Windows
    installations) into a temporary file, so ``--ssl`` works out of the box.
    """
    if not certfile:
        certfile, keyfile = _generate_self_signed_cert()

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile, keyfile)
    return ctx


def _generate_self_signed_cert() -> "tuple[str, str]":
    """Generate a self-signed cert/key pair and return their (cert, key) paths."""
    import subprocess
    import tempfile
    import os

    cert_fd, certfile = tempfile.mkstemp(suffix=".pem", prefix="netconnect-cert-")
    key_fd, keyfile = tempfile.mkstemp(suffix=".pem", prefix="netconnect-key-")
    os.close(cert_fd)
    os.close(key_fd)
    subprocess.run(
        [
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
            "-keyout", keyfile, "-out", certfile,
            "-days", "3650", "-subj", "/CN=NetConnect",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return certfile, keyfile


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


def parse_port_range(spec: str) -> List[int]:
    """Parse a port spec into a flat list of ints.

    Accepts: '80', '80,443', '8080-8090', '80,8080-8090', '1000-1002,2000'.
    Single values outside 1-65535 or a reversed range are clamped/swapped.
    """
    ports: List[int] = []
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            lo, hi = int(a.strip()), int(b.strip())
            if lo > hi:
                lo, hi = hi, lo
            ports.extend(range(lo, hi + 1))
        else:
            ports.append(int(part))
    # De-duplicate, keep order, validate range
    seen = set()
    result = []
    for p in ports:
        if 1 <= p <= 65535 and p not in seen:
            seen.add(p)
            result.append(p)
    return result


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


def create_tcp_listener(port: int, host: str = '0.0.0.0', ssl_context: Optional['ssl.SSLContext'] = None) -> Optional[socket.socket]:
    """Create a TCP listener on specified port.

    If ``ssl_context`` is provided the accepted connections are wrapped in TLS.
    """
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


def create_listeners(ports: List[int], protocol: Protocol = Protocol.BOTH, ssl_context: Optional['ssl.SSLContext'] = None) -> List[PortListener]:
    """Create listeners on specified ports."""
    listeners = []
    for port in ports:
        if protocol in (Protocol.TCP, Protocol.BOTH):
            sock = create_tcp_listener(port, ssl_context=ssl_context)
            if sock:
                listeners.append(PortListener(port=port, protocol=Protocol.TCP, socket=sock, ssl_context=ssl_context))
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
    """Run listeners for specified duration (seconds) or indefinitely.

    On a successful TCP accept the listener sends an identification banner
    (so tools like curl/telnet/nc receive a response), wraps the socket in
    TLS when the listener carries an ``ssl_context``, and echoes any received
    data back to the client.
    """
    import select
    import sys

    def handle_tcp(listener: PortListener, conn: "socket.socket", addr) -> None:
        client_str = f"{addr[0]}:{addr[1]}"
        banner = banner_text().encode()
        try:
            if listener.ssl_context is not None:
                conn = listener.ssl_context.wrap_socket(conn, server_side=True)
                print(f"TLS connection from {client_str} on port {listener.port}")
            else:
                print(f"TCP connection from {client_str} on port {listener.port}")
            # Send banner immediately so interactive clients (telnet/nc/curl)
            # see it. Note: Test-NetConnection / port scanners never read
            # server data, so they will not display this banner.
            conn.sendall(banner)
            print(f"  -> sent banner: {banner.decode().strip()!r}")
            conn.settimeout(5.0)
            try:
                data = conn.recv(4096)
                if data:
                    # Echo back to prove a live, responsive service
                    conn.sendall(data)
            except (socket.timeout, OSError):
                pass
        except OSError as e:
            print(f"Error handling {client_str}: {e}", file=sys.stderr)
        finally:
            try:
                conn.close()
            except OSError:
                pass

    sockets = [l.socket for l in listeners if l.socket]
    if not sockets:
        print("No listeners created")
        return

    print(f"Listening on {len(sockets)} socket(s)... Press Ctrl+C to stop")
    print("Clients (telnet/nc/curl) receive an identification banner on connect.")
    print("Note: Test-NetConnection and port scanners check reachability only and")
    print("      will NOT display the banner (they never read server responses).")
    if duration:
        print(f"Will stop after {duration} seconds")

    start_time = time.time()
    try:
        while True:
            if duration and (time.time() - start_time) >= duration:
                print(f"\nDuration {duration}s reached, stopping...")
                break

            ready, _, _ = select.select(sockets, [], [], 1.0)
            for sock in ready:
                listener = next(l for l in listeners if l.socket is sock)
                try:
                    if sock.type == socket.SOCK_STREAM:
                        conn, addr = sock.accept()
                        handle_tcp(listener, conn, addr)
                    else:
                        data, addr = sock.recvfrom(1024)
                        print(f"UDP packet from {addr[0]}:{addr[1]} on port {sock.getsockname()[1]} ({len(data)} bytes)")
                except OSError:
                    pass
    except KeyboardInterrupt:
        print("\nStopped by user")