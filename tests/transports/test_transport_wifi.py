"""
Unit tests for obdii.transports.transport_wifi module.
"""
import pytest

from socket import error as s_error

from obdii.basetypes import MISSING
from obdii.transports.transport_wifi import TransportWifi


class TestTransportWifiInit:
    """Test suite for TransportWifi initialization."""

    def test_init_with_required_parameters(self):
        """Test initialization with required address and port."""
        transport = TransportWifi(address="192.168.0.10", port=35000)

        assert transport.address == "192.168.0.10"
        assert transport.port == 35000
        assert transport.timeout == 5.0
        assert transport.socket_conn is None

    @pytest.mark.parametrize(
        ("address", "port", "timeout"),
        [
            ("192.168.1.1", 35000, 5.0),
            ("10.0.0.1", 23, 10.0),
            ("172.16.0.1", "35000", 2.0),
            ("192.168.0.10", 8080, 15.0),
        ],
        ids=["default", "telnet", "string_port", "http_port"],
    )
    def test_init_with_custom_parameters(self, address, port, timeout):
        """Test initialization with custom parameters."""
        transport = TransportWifi(address=address, port=port, timeout=timeout)

        assert transport.address == address
        assert transport.port == port
        assert transport.timeout == timeout

    def test_init_without_address_raises_error(self):
        """Test that initialization without address raises ValueError."""
        with pytest.raises(ValueError, match="Both address and port must be specified"):
            TransportWifi(port=35000)

    def test_init_without_port_raises_error(self):
        """Test that initialization without port raises ValueError."""
        with pytest.raises(ValueError, match="Both address and port must be specified"):
            TransportWifi(address="192.168.0.10")

    def test_init_without_both_raises_error(self):
        """Test that initialization without address and port raises ValueError."""
        with pytest.raises(ValueError, match="Both address and port must be specified"):
            TransportWifi()

    def test_init_with_missing_values_raises_error(self):
        """Test that initialization with MISSING values raises ValueError."""
        with pytest.raises(ValueError, match="Both address and port must be specified"):
            TransportWifi(address=MISSING, port=MISSING)

    def test_overridable_attributes_structure(self):
        """Test that overridable_attributes contains expected keys."""
        transport = TransportWifi(address="192.168.0.10", port=35000)

        assert "address" in transport.overridable_attributes
        assert "port" in transport.overridable_attributes
        assert "timeout" in transport.overridable_attributes


class TestTransportWifiRepr:
    """Test suite for TransportWifi __repr__ method."""

    @pytest.mark.parametrize(
        ("address", "port", "expected_addr", "expected_port"),
        [
            ("192.168.0.10", 35000, "192.168.0.10", "35000"),
            ("10.0.0.1", 23, "10.0.0.1", "23"),
            ("172.16.0.1", "8080", "172.16.0.1", "8080"),
        ],
        ids=["default", "telnet", "string_port"],
    )
    def test_repr_format(self, address, port, expected_addr, expected_port):
        """Test __repr__ format with various configurations."""
        transport = TransportWifi(address=address, port=port)
        result = repr(transport)

        assert "TransportWifi" in result
        assert expected_addr in result
        assert expected_port in result
        assert ':' in result


class TestTransportWifiIsConnected:
    """Test suite for TransportWifi is_connected method."""

    def test_not_connected_when_socket_none(self):
        """Test is_connected returns False when socket_conn is None."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        
        assert transport.is_connected() is False

    def test_connected_when_socket_has_peer(self, mocker):
        """Test is_connected returns True when socket has peer."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        mock_socket.getpeername.return_value = ("192.168.0.10", 35000)
        transport.socket_conn = mock_socket

        assert transport.is_connected() is True

    def test_not_connected_when_socket_error(self, mocker):
        """Test is_connected returns False when getpeername raises socket error."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        mock_socket.getpeername.side_effect = s_error("Not connected")
        transport.socket_conn = mock_socket

        assert transport.is_connected() is False


class TestTransportWifiConnect:
    """Test suite for TransportWifi connect method."""

    def test_connect_creates_socket_connection(self, mocker):
        """Test connect creates a socket connection."""
        mock_socket_class = mocker.patch("obdii.transports.transport_wifi.socket")
        mock_socket_instance = mocker.MagicMock()
        mock_socket_class.return_value = mock_socket_instance
        transport = TransportWifi(address="192.168.0.10", port=35000)

        transport.connect()

        mock_socket_instance.settimeout.assert_called_once_with(5.0)
        mock_socket_instance.connect.assert_called_once_with(("192.168.0.10", 35000))
        assert transport.socket_conn == mock_socket_instance

    def test_connect_with_override_parameters(self, mocker):
        """Test connect with override parameters."""
        mock_socket_class = mocker.patch("obdii.transports.transport_wifi.socket")
        mock_socket_instance = mocker.MagicMock()
        mock_socket_class.return_value = mock_socket_instance
        transport = TransportWifi(address="192.168.0.10", port=35000)

        transport.connect(timeout=10.0)

        mock_socket_instance.settimeout.assert_called_once_with(10.0)
        mock_socket_instance.connect.assert_called_once_with(("192.168.0.10", 35000))

    def test_connect_with_string_port(self, mocker):
        """Test connect converts string port to int."""
        mock_socket_class = mocker.patch("obdii.transports.transport_wifi.socket")
        mock_socket_instance = mocker.MagicMock()
        mock_socket_class.return_value = mock_socket_instance
        transport = TransportWifi(address="192.168.0.10", port="35000")

        transport.connect()

        mock_socket_instance.connect.assert_called_once_with(("192.168.0.10", 35000))

    @pytest.mark.parametrize(
        ("address", "port"),
        [
            ("192.168.1.1", 35000),
            ("10.0.0.1", 23),
            ("172.16.0.1", "8080"),
        ],
        ids=["default", "telnet", "string_port"],
    )
    def test_connect_various_addresses(self, mocker, address, port):
        """Test connect with various address and port combinations."""
        mock_socket_class = mocker.patch("obdii.transports.transport_wifi.socket")
        mock_socket_instance = mocker.MagicMock()
        mock_socket_class.return_value = mock_socket_instance
        transport = TransportWifi(address=address, port=port)

        transport.connect()

        mock_socket_instance.connect.assert_called_once_with((address, int(port)))


class TestTransportWifiClose:
    """Test suite for TransportWifi close method."""

    def test_close_when_connected(self, mocker):
        """Test close when connection is open."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        transport.socket_conn = mock_socket

        transport.close()

        mock_socket.close.assert_called_once()
        assert transport.socket_conn is None

    def test_close_when_not_connected(self):
        """Test close when socket_conn is None."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        transport.socket_conn = None

        transport.close()

        assert transport.socket_conn is None


class TestTransportWifiWriteBytes:
    """Test suite for TransportWifi write_bytes method."""

    def test_write_bytes_success(self, mocker):
        """Test successful write operation."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        transport.socket_conn = mock_socket
        query = b"ATZ\r"

        transport.write_bytes(query)

        mock_socket.sendall.assert_called_once_with(query)

    def test_write_bytes_when_not_connected(self):
        """Test write_bytes raises RuntimeError when not connected."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        transport.socket_conn = None

        with pytest.raises(RuntimeError, match="Socket is not connected"):
            transport.write_bytes(b"ATZ\r")

    @pytest.mark.parametrize(
        "query",
        [
            b"ATZ\r",
            b"ATI\r",
            b"01 00\r",
            b"",
            b'\r',
        ],
        ids=["ATZ", "ATI", "mode_01", "empty", "single_cr"],
    )
    def test_write_bytes_various_commands(self, mocker, query):
        """Test write_bytes with various command patterns."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        transport.socket_conn = mock_socket

        transport.write_bytes(query)

        mock_socket.sendall.assert_called_once_with(query)


class TestTransportWifiReadBytes:
    """Test suite for TransportWifi read_bytes method."""

    def test_read_bytes_default_terminator(self, mocker):
        """Test read_bytes with default terminator '>'."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        mock_socket.recv.side_effect = [b'O', b'K', b'\r', b'>']
        transport.socket_conn = mock_socket

        result = transport.read_bytes()

        assert result == b"OK\r>"
        assert mock_socket.recv.call_count == 4

    def test_read_bytes_custom_terminator(self, mocker):
        """Test read_bytes with custom terminator."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        mock_socket.recv.side_effect = [b'O', b'K', b'\r', b'\n']
        transport.socket_conn = mock_socket

        result = transport.read_bytes(expected_seq=b"\r\n")

        assert result == b"OK\r\n"
        assert mock_socket.recv.call_count == 4

    def test_read_bytes_with_size_limit(self, mocker):
        """Test read_bytes with size parameter."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        mock_socket.recv.side_effect = [b'A', b'B', b'C']
        transport.socket_conn = mock_socket

        result = transport.read_bytes(size=3)

        assert result == b"ABC"
        assert mock_socket.recv.call_count == 3

    def test_read_bytes_when_not_connected(self):
        """Test read_bytes raises RuntimeError when not connected."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        transport.socket_conn = None

        with pytest.raises(RuntimeError, match="Socket is not connected"):
            transport.read_bytes()

    def test_read_bytes_connection_closed(self, mocker):
        """Test read_bytes raises RuntimeError when connection closes."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        mock_socket.recv.return_value = b""
        transport.socket_conn = mock_socket

        with pytest.raises(RuntimeError, match="Socket connection closed"):
            transport.read_bytes()

    @pytest.mark.parametrize(
        ("expected_seq", "recv_data"),
        [
            (b'>', [b'4', b'1', b' ', b'0', b'0', b'>']),
            (b"\r\n", [b'O', b'K', b'\r', b'\n']),
            (b">>", [b'>', b'>']),
        ],
        ids=["prompt", "crlf", "double_prompt"],
    )
    def test_read_bytes_various_terminators(self, mocker, expected_seq, recv_data):
        """Test read_bytes with various terminators."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        mock_socket.recv.side_effect = recv_data
        transport.socket_conn = mock_socket

        result = transport.read_bytes(expected_seq=expected_seq)

        assert result == b"".join(recv_data)
        assert mock_socket.recv.call_count == len(recv_data)

    def test_read_bytes_multi_byte_terminator(self, mocker):
        """Test read_bytes with multi-byte terminator sequence."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        mock_socket.recv.side_effect = [b'T', b'E', b'S', b'T', b'>', b'>']
        transport.socket_conn = mock_socket

        result = transport.read_bytes(expected_seq=b">>")

        assert result == b"TEST>>"

    def test_read_bytes_size_reached_before_terminator(self, mocker):
        """Test read_bytes stops at size limit before finding terminator."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        mock_socket.recv.side_effect = [b'A', b'B', b'C', b'D', b'E']
        transport.socket_conn = mock_socket

        result = transport.read_bytes(expected_seq=b'>', size=5)

        assert result == b"ABCDE"
        assert mock_socket.recv.call_count == 5

    def test_read_bytes_empty_terminator(self, mocker):
        """Test read_bytes with empty terminator."""
        transport = TransportWifi(address="192.168.0.10", port=35000)
        mock_socket = mocker.MagicMock()
        mock_socket.recv.side_effect = [b'O', b'K']
        transport.socket_conn = mock_socket

        result = transport.read_bytes(expected_seq=b"", size=2)

        assert result == b"OK"
