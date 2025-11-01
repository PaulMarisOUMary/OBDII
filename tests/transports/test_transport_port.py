"""
Unit tests for obdii.transports.transport_port module.
"""
import pytest

from obdii.basetypes import MISSING
from obdii.transports.transport_port import TransportPort


class TestTransportPortInit:
    """Test suite for TransportPort initialization."""

    def test_init_with_required_parameters(self):
        """Test initialization with required port parameter."""
        transport = TransportPort(port="COM3")

        assert transport.port == "COM3"
        assert transport.baudrate == 38400
        assert transport.timeout == 5.0
        assert transport.write_timeout == 3.0
        assert transport.serial_conn is None

    @pytest.mark.parametrize(
        ("port", "baudrate", "timeout", "write_timeout"),
        [
            ("COM1", 9600, 10.0, 5.0),
            ("COM3", 38400, 5.0, 3.0),
            ("/dev/ttyUSB0", 115200, 2.0, 1.0),
            ("/dev/ttyAMA0", 19200, 15.0, 10.0),
        ],
        ids=["COM1", "COM3", "USB0", "AMA0"],
    )
    def test_init_with_custom_parameters(self, port, baudrate, timeout, write_timeout):
        """Test initialization with custom parameters."""
        transport = TransportPort(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
            write_timeout=write_timeout,
        )

        assert transport.port == port
        assert transport.baudrate == baudrate
        assert transport.timeout == timeout
        assert transport.write_timeout == write_timeout

    def test_init_without_port_raises_error(self):
        """Test that initialization without port raises ValueError."""
        with pytest.raises(ValueError, match="Port must be specified"):
            TransportPort()

    def test_init_with_missing_port_raises_error(self):
        """Test that initialization with MISSING port raises ValueError."""
        with pytest.raises(ValueError, match="Port must be specified"):
            TransportPort(port=MISSING)

    def test_overridable_attributes_structure(self):
        """Test that overridable_attributes contains expected keys."""
        transport = TransportPort(port="COM3")

        assert "port" in transport.overridable_attributes
        assert "baudrate" in transport.overridable_attributes
        assert "timeout" in transport.overridable_attributes
        assert "write_timeout" in transport.overridable_attributes


class TestTransportPortRepr:
    """Test suite for TransportPort __repr__ method."""

    @pytest.mark.parametrize(
        ("port", "baudrate", "expected_port", "expected_baud"),
        [
            ("COM3", 38400, "COM3", "38400"),
            ("COM1", 9600, "COM1", "9600"),
            ("/dev/ttyUSB0", 115200, "/dev/ttyUSB0", "115200"),
        ],
        ids=["COM3", "COM1", "USB0"],
    )
    def test_repr_format(self, port, baudrate, expected_port, expected_baud):
        """Test __repr__ format with various port configurations."""
        transport = TransportPort(port=port, baudrate=baudrate)
        result = repr(transport)

        assert "TransportPort" in result
        assert expected_port in result
        assert expected_baud in result
        assert "baud" in result


class TestTransportPortIsConnected:
    """Test suite for TransportPort is_connected method."""

    def test_not_connected_when_serial_none(self):
        """Test is_connected returns False when serial_conn is None."""
        transport = TransportPort(port="COM3")
        
        assert transport.is_connected() is False

    def test_connected_when_serial_open(self, mocker):
        """Test is_connected returns True when serial is open."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        transport.serial_conn = mock_serial

        assert transport.is_connected() is True

    def test_not_connected_when_serial_closed(self, mocker):
        """Test is_connected returns False when serial is closed."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = False
        transport.serial_conn = mock_serial

        assert transport.is_connected() is False


class TestTransportPortConnect:
    """Test suite for TransportPort connect method."""

    def test_connect_creates_serial_connection(self, mocker):
        """Test connect creates a Serial connection."""
        mock_serial_class = mocker.patch("obdii.transports.transport_port.Serial")
        transport = TransportPort(port="COM3")

        transport.connect()

        mock_serial_class.assert_called_once_with(
            port="COM3",
            baudrate=38400,
            timeout=5.0,
            write_timeout=3.0,
        )
        assert transport.serial_conn == mock_serial_class.return_value

    def test_connect_creates_serial_with_defaults(self, mocker):
        """Test connect creates Serial with transport defaults."""
        mock_serial_class = mocker.patch("obdii.transports.transport_port.Serial")
        transport = TransportPort(port="COM3", baudrate=115200, timeout=10.0)

        transport.connect()

        mock_serial_class.assert_called_once()
        assert transport.serial_conn == mock_serial_class.return_value

    def test_connect_with_extra_kwargs(self, mocker):
        """Test connect with extra Serial parameters."""
        mock_serial_class = mocker.patch("obdii.transports.transport_port.Serial")
        transport = TransportPort(port="COM3")

        transport.connect(parity='N', stopbits=1)

        call_kwargs = mock_serial_class.call_args[1]
        assert call_kwargs["parity"] == 'N'
        assert call_kwargs["stopbits"] == 1


class TestTransportPortClose:
    """Test suite for TransportPort close method."""

    def test_close_when_connected(self, mocker):
        """Test close when connection is open."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        transport.serial_conn = mock_serial

        transport.close()

        mock_serial.close.assert_called_once()
        assert transport.serial_conn is None

    def test_close_when_already_closed(self, mocker):
        """Test close when connection is already closed."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = False
        transport.serial_conn = mock_serial

        transport.close()

        mock_serial.close.assert_not_called()
        assert transport.serial_conn is None

    def test_close_when_not_connected(self):
        """Test close when serial_conn is None."""
        transport = TransportPort(port="COM3")
        transport.serial_conn = None

        transport.close()

        assert transport.serial_conn is None


class TestTransportPortWriteBytes:
    """Test suite for TransportPort write_bytes method."""

    def test_write_bytes_success(self, mocker):
        """Test successful write operation."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        query = b"ATZ\r"
        mock_serial.write.return_value = len(query)
        transport.serial_conn = mock_serial

        transport.write_bytes(query)

        mock_serial.reset_input_buffer.assert_called_once()
        mock_serial.write.assert_called_once_with(query)
        mock_serial.flush.assert_called_once()

    def test_write_bytes_when_not_connected(self):
        """Test write_bytes raises RuntimeError when not connected."""
        transport = TransportPort(port="COM3")
        transport.serial_conn = None

        with pytest.raises(RuntimeError, match="Serial port is not connected"):
            transport.write_bytes(b"ATZ\r")

    def test_write_bytes_when_closed(self, mocker):
        """Test write_bytes raises RuntimeError when port is closed."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = False
        transport.serial_conn = mock_serial

        with pytest.raises(RuntimeError, match="Serial port is not connected"):
            transport.write_bytes(b"ATZ\r")

    def test_write_bytes_partial_write(self, mocker):
        """Test write_bytes raises IOError on partial write."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        mock_serial.write.return_value = 5
        transport.serial_conn = mock_serial
        query = b"ATZ\r\n\r\n"

        with pytest.raises(IOError, match="Failed to write all bytes"):
            transport.write_bytes(query)

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
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        mock_serial.write.return_value = len(query)
        transport.serial_conn = mock_serial

        transport.write_bytes(query)

        mock_serial.write.assert_called_once_with(query)


class TestTransportPortReadBytes:
    """Test suite for TransportPort read_bytes method."""

    def test_read_bytes_default_terminator(self, mocker):
        """Test read_bytes with default terminator '>'."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        mock_serial.read_until.return_value = b"OK\r>"
        transport.serial_conn = mock_serial

        result = transport.read_bytes()

        mock_serial.read_until.assert_called_once_with(b'>', None)
        assert result == b"OK\r>"

    def test_read_bytes_custom_terminator(self, mocker):
        """Test read_bytes with custom terminator."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        mock_serial.read_until.return_value = b"OK\r\n"
        transport.serial_conn = mock_serial

        result = transport.read_bytes(expected_seq=b"\r\n")

        mock_serial.read_until.assert_called_once_with(b"\r\n", None)
        assert result == b"OK\r\n"

    def test_read_bytes_with_size_limit(self, mocker):
        """Test read_bytes with size parameter."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        mock_serial.read_until.return_value = b"OK"
        transport.serial_conn = mock_serial

        result = transport.read_bytes(size=100)

        mock_serial.read_until.assert_called_once_with(b'>', 100)
        assert result == b"OK"

    def test_read_bytes_when_not_connected(self):
        """Test read_bytes raises RuntimeError when not connected."""
        transport = TransportPort(port="COM3")
        transport.serial_conn = None

        with pytest.raises(RuntimeError, match="Serial port is not connected"):
            transport.read_bytes()

    def test_read_bytes_when_closed(self, mocker):
        """Test read_bytes raises RuntimeError when port is closed."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = False
        transport.serial_conn = mock_serial

        with pytest.raises(RuntimeError, match="Serial port is not connected"):
            transport.read_bytes()

    @pytest.mark.parametrize(
        ("expected_seq", "response"),
        [
            (b'>', b"41 00 BE 3E B8 11\r>"),
            (b"\r\n", b"OK\r\n"),
            (b"STOPPED\r", b"STOPPED\r"),
        ],
        ids=["prompt", "crlf", "stopped"],
    )
    def test_read_bytes_various_terminators(self, mocker, expected_seq, response):
        """Test read_bytes with various terminators."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        mock_serial.read_until.return_value = response
        transport.serial_conn = mock_serial

        result = transport.read_bytes(expected_seq=expected_seq)

        mock_serial.read_until.assert_called_once()
        assert result == response

    def test_read_bytes_multi_byte_terminator(self, mocker):
        """Test read_bytes with multi-byte terminator sequence."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        mock_serial.read_until.return_value = b"TEST>>"
        transport.serial_conn = mock_serial

        result = transport.read_bytes(expected_seq=b">>")

        mock_serial.read_until.assert_called_once_with(b">>", None)
        assert result == b"TEST>>"

    def test_read_bytes_empty_terminator(self, mocker):
        """Test read_bytes with empty terminator and size limit."""
        transport = TransportPort(port="COM3")
        mock_serial = mocker.MagicMock()
        mock_serial.is_open = True
        mock_serial.read_until.return_value = b"OK"
        transport.serial_conn = mock_serial

        result = transport.read_bytes(expected_seq=b"", size=2)

        mock_serial.read_until.assert_called_once_with(b"", 2)
        assert result == b"OK"
