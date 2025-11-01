"""
Unit tests for obdii.utils.scan module.
"""
from obdii.utils.scan import scan_transports, scan_ports, scan_wifi
from obdii.transports.transport_base import TransportBase
from obdii.transports.transport_wifi import TransportWifi


class TestScanTransports:
    """Test suite for scan_transports function."""

    def test_finds_devices_with_valid_responses(self, mocker):
        """Test successful device discovery with ELM327 and prompt responses."""
        mock_transport1 = mocker.Mock(spec=TransportBase)
        mock_transport1.read_bytes.return_value = b"ELM327 v1.5"
        mock_transport2 = mocker.Mock(spec=TransportBase)
        mock_transport2.read_bytes.return_value = b'>'
        
        mock_cls = mocker.Mock(side_effect=[mock_transport1, mock_transport2])
        candidates = [{"port": "COM3"}, {"port": "COM4"}]
        
        result = scan_transports(candidates, mock_cls)
        
        assert len(result) == 2
        mock_transport1.connect.assert_called_once()
        mock_transport1.write_bytes.assert_called_once()

    def test_return_first_stops_after_one(self, mocker):
        """Test return_first parameter stops scanning after first valid device."""
        mock_transport = mocker.Mock(spec=TransportBase)
        mock_transport.read_bytes.return_value = b"ELM327 v1.5"
        mock_cls = mocker.Mock(return_value=mock_transport)
        
        result = scan_transports([{"port": "COM3"}, {"port": "COM4"}], mock_cls, return_first=True)
        
        assert len(result) == 1
        assert mock_cls.call_count == 1

    def test_error_handling_and_cleanup(self, mocker):
        """Test various errors are handled and transport is closed."""
        scenarios = [
            (Exception("Connection failed"), 'connect'),
            (Exception("Write failed"), 'write_bytes'),
            (Exception("Read failed"), 'read_bytes'),
        ]
        
        for error, method in scenarios:
            mock_transport = mocker.Mock(spec=TransportBase)
            getattr(mock_transport, method).side_effect = error
            mock_cls = mocker.Mock(return_value=mock_transport)
            
            result = scan_transports([{"port": "COM3"}], mock_cls)
            
            assert result == []
            mock_transport.close.assert_called()

    def test_invalid_response_rejected(self, mocker):
        """Test devices with invalid responses are filtered out."""
        mock_transport = mocker.Mock(spec=TransportBase)
        mock_transport.read_bytes.return_value = b"INVALID"
        mock_cls = mocker.Mock(return_value=mock_transport)
        
        result = scan_transports([{"port": "COM3"}], mock_cls)
        
        assert result == []
        mock_transport.close.assert_called()

    def test_custom_probe_and_kwargs(self, mocker):
        """Test custom probe bytes and kwargs forwarding."""
        mock_transport = mocker.Mock(spec=TransportBase)
        mock_transport.read_bytes.return_value = b"ELM327"
        mock_cls = mocker.Mock(return_value=mock_transport)
        
        result = scan_transports([{"port": "COM3"}], mock_cls, probe=b"TEST", timeout=5)
        
        assert len(result) == 1
        mock_transport.write_bytes.assert_called_once_with(b"TEST")
        mock_transport.connect.assert_called_once_with(timeout=5)


class TestScanPorts:
    """Test suite for scan_ports function."""

    def test_scan_ports_basic_functionality(self, mocker):
        """Test basic port scanning and parameter forwarding."""
        mock_port = mocker.Mock()
        mock_port.device = "COM3"
        mocker.patch("serial.tools.list_ports.comports", return_value=[mock_port])
        mock_scan = mocker.patch("obdii.utils.scan.scan_transports", return_value=["device"])
        
        result = scan_ports(return_first=False, timeout=10)
        
        assert result == ["device"]
        candidates = mock_scan.call_args[0][0]
        assert {"port": "COM3"} in candidates
        assert mock_scan.call_args[1]["return_first"] is False
        assert mock_scan.call_args[1]["timeout"] == 10

    def test_linux_pts_ports(self, mocker):
        """Test Linux /dev/pts/* port inclusion (excluding ptmx)."""
        mocker.patch("platform.system", return_value="Linux")
        mocker.patch("serial.tools.list_ports.comports", return_value=[])
        mocker.patch("obdii.utils.scan.glob", return_value=["/dev/pts/1", "/dev/pts/ptmx"])
        mock_scan = mocker.patch("obdii.utils.scan.scan_transports", return_value=[])
        
        scan_ports()
        
        candidates = mock_scan.call_args[0][0]
        assert {"port": "/dev/pts/1"} in candidates
        assert {"port": "/dev/pts/ptmx"} not in candidates


class TestScanWifi:
    """Test suite for scan_wifi function."""

    def test_scan_wifi_basic_functionality(self, mocker):
        """Test WiFi scanning with common addresses and parameter forwarding."""
        mock_scan = mocker.patch("obdii.utils.scan.scan_transports", return_value=["device"])
        
        result = scan_wifi(return_first=False, timeout=15)
        
        assert result == ["device"]
        candidates = mock_scan.call_args[0][0]
        assert {"address": "192.168.0.10", "port": 35000} in candidates
        assert {"address": "192.168.1.10", "port": 35000} in candidates
        assert {"address": "192.168.0.74", "port": 23} in candidates
        assert len(candidates) == 3
        assert mock_scan.call_args[0][1] == TransportWifi
        assert mock_scan.call_args[1]["return_first"] is False
        assert mock_scan.call_args[1]["timeout"] == 15
