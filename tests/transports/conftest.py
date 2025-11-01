"""
Shared fixtures for transports tests.
"""
import pytest


@pytest.fixture
def mock_serial_conn(mocker):
    """Create a mock Serial connection."""
    mock = mocker.MagicMock()
    mock.is_open = True
    mock.write.return_value = 10
    mock.read_until.return_value = b"OK\r>"
    return mock


@pytest.fixture
def mock_socket_conn(mocker):
    """Create a mock socket connection."""
    mock = mocker.MagicMock()
    mock.getpeername.return_value = ("192.168.0.10", 35000)
    mock.recv.side_effect = [b'O', b'K', b'\r', b'>']
    return mock


@pytest.fixture
def serial_port_kwargs():
    """Standard kwargs for TransportPort."""
    return {
        "port": "COM3",
        "baudrate": 38400,
        "timeout": 5.0,
        "write_timeout": 3.0,
    }


@pytest.fixture
def wifi_kwargs():
    """Standard kwargs for TransportWifi."""
    return {
        "address": "192.168.0.10",
        "port": 35000,
        "timeout": 5.0,
    }
