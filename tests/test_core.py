"""Tests for NetConnect core functionality."""

import pytest
from netconnect.core import (
    parse_ip_range,
    Protocol,
    create_tcp_listener,
    create_udp_listener,
    create_listeners,
    close_listeners,
)


def test_parse_ip_range_single():
    """Test parsing single IP."""
    result = parse_ip_range("192.168.1.100")
    assert result == ["192.168.1.100"]


def test_parse_ip_range_valid():
    """Test parsing valid IP range."""
    result = parse_ip_range("192.168.1.100-192.168.1.102")
    assert result == ["192.168.1.100", "192.168.1.101", "192.168.1.102"]


def test_parse_ip_range_reversed():
    """Test parsing reversed IP range (should swap)."""
    result = parse_ip_range("192.168.1.102-192.168.1.100")
    assert result == ["192.168.1.100", "192.168.1.101", "192.168.1.102"]


def test_parse_ip_range_single_same():
    """Test parsing range with same start/end."""
    result = parse_ip_range("10.0.0.1-10.0.0.1")
    assert result == ["10.0.0.1"]


def test_protocol_enum():
    """Test Protocol enum values."""
    assert Protocol.TCP.value == "tcp"
    assert Protocol.UDP.value == "udp"
    assert Protocol.BOTH.value == "both"


def test_create_tcp_listener():
    """Test creating TCP listener."""
    sock = create_tcp_listener(0)  # Port 0 = auto-assign
    assert sock is not None
    sock.close()


def test_create_udp_listener():
    """Test creating UDP listener."""
    sock = create_udp_listener(0)
    assert sock is not None
    sock.close()


def test_create_listeners():
    """Test creating multiple listeners."""
    listeners = create_listeners([0, 0], Protocol.BOTH)  # Auto-assign ports
    assert len(listeners) >= 2  # At least TCP + UDP for each port
    close_listeners(listeners)


def test_close_listeners():
    """Test closing listeners."""
    listeners = create_listeners([0], Protocol.TCP)
    close_listeners(listeners)  # Should not raise


if __name__ == "__main__":
    pytest.main([__file__, "-v"])