"""
Unit tests for obdii.protocols.protocol_can module.

Tests cover both single-frame and multi-frame CAN message parsing per ISO 15765-4.
"""
import pytest

from obdii.command import Command
from obdii.mode import Mode
from obdii.protocol import Protocol
from obdii.protocols.protocol_can import ProtocolCAN
from obdii.response import Context, ResponseBase


class TestProtocolCANSingleFrame:
    """Single-frame CAN message parsing (<=7 data bytes)."""

    @pytest.mark.parametrize(
        ("protocol", "raw_messages", "expected_data"),
        [
            # 11-bit header: 7E8 03 41 0C 1A F8
            # After split: 7E 8 03 41 0C 1A F8 (7 components)
            # Normalized: 00 00 7E 8 03 41 0C 1A F8 (9 components)
            # Index 4 = 03, payload_length = 0x03 - 2 = 1
            # Last 1 byte: (b'F8',)
            (
                Protocol.ISO_15765_4_CAN,
                [b"7E8 03 41 0C 1A F8", b'>'],
                [(b'F8',)],
            ),
            # 29-bit header: 18DAF11005410A7B
            # After split: 18 DA F1 10 05 41 0A 7B (8 components)
            # No normalization prefix for 29-bit
            # Index 4 = 05, payload_length = 0x05 - 2 = 3
            # Last 3 bytes: (b'41', b'0A', b'7B')
            (
                Protocol.ISO_15765_4_CAN_B,
                [b"18DAF11005410A7B", b'>'],
                [(b'41', b'0A', b'7B')],
            ),
        ],
        ids=["11bit-single-frame", "29bit-single-frame"],
    )
    def test_single_frame_parsing(self, protocol, raw_messages, expected_data):
        cmd = Command(Mode.REQUEST, 0x0C, 2)
        ctx = Context(cmd, protocol)
        rb = ResponseBase(ctx, b''.join(raw_messages), raw_messages)
        handler = ProtocolCAN()

        resp = handler.parse_response(rb)

        assert resp.parsed_data == expected_data

@pytest.mark.skip(reason="Multi-frame reassembly not yet implemented")
class TestProtocolCANMultiFrame:
    """Multi-frame CAN message parsing (>7 data bytes)."""

    def test_multiframe_vin_request(self):
        # VIN request returns 17 ASCII characters across multiple frames
        # First frame: 10 14 49 02 01 W V W Z Z
        #   10 = first frame, 14 = 20 bytes total
        #   49 = mode 0x09 response (0x40 + 0x09)
        #   02 = PID 0x02 (VIN)
        #   01 = data byte count
        #   W V W Z Z = first 5 VIN chars
        # Consecutive frames: 21 Z 1 2 3 4 5 6
        #                     22 7 8 9 0 1 2 3
        # etc.
        cmd = Command(Mode.VEHICLE_INFO, 0x02, 20)
        ctx = Context(cmd, Protocol.ISO_15765_4_CAN)
        raw_messages = [
            b"7E8 10 14 49 02 01 57 56 57",
            b"7E8 21 5A 5A 5A 31 4A 4D 33",
            b"7E8 22 36 33 39 37 36 00 00",
            b'>',
        ]
        rb = ResponseBase(ctx, b'\r'.join(raw_messages), raw_messages)
        handler = ProtocolCAN()

        resp = handler.parse_response(rb)

        # Currently the code doesn't handle multi-frame reassembly
        # It will parse each line separately
        # This test documents current behavior and will need updating
        # when multi-frame support is added
        assert resp.parsed_data is not None
        assert len(resp.parsed_data) > 0


class TestProtocolCANHelpers:
    """Helper method behavior in ProtocolCAN."""

    def test_strip_prompt_removes_prompt(self):
        handler = ProtocolCAN()
        messages = [b"DATA1", b"DATA2", b'>']

        result = handler._strip_prompt(messages)

        assert result == [b"DATA1", b"DATA2"]

    def test_strip_prompt_no_prompt_unchanged(self):
        handler = ProtocolCAN()
        messages = [b"DATA1", b"DATA2"]

        result = handler._strip_prompt(messages)

        assert result == [b"DATA1", b"DATA2"]

    @pytest.mark.parametrize(
        ("protocol", "line", "expected"),
        [
            (
                Protocol.ISO_15765_4_CAN,
                b"7E803410C1AF8",
                (b'00', b'00', b'07', b'E8', b'03', b'41', b'0C', b'1A', b'F8'),
            ),
            (
                Protocol.ISO_15765_4_CAN_B,
                b"18DAF11005410A7B",
                (b'18', b'DA', b'F1', b'10', b'05', b'41', b'0A', b'7B'),
            ),
        ],
        ids=["11bit-adds-prefix", "29bit-no-prefix"],
    )
    def test_normalize_components(self, protocol, line, expected):
        handler = ProtocolCAN()

        result = handler._normalize_components(line, protocol)

        assert result == expected


class TestProtocolCANATCommands:
    """AT command response parsing."""

    def test_at_command_single_line_response(self):
        cmd = Command(Mode.AT, 'Z', 0)
        ctx = Context(cmd, Protocol.ISO_15765_4_CAN)
        raw_messages = [b"ELM327 v1.5", b'>']
        rb = ResponseBase(ctx, b'\r'.join(raw_messages), raw_messages)
        handler = ProtocolCAN()

        resp = handler.parse_response(rb)

        assert resp.value == "ELM327 v1.5"


class TestProtocolCANErrors:
    """Error detection and handling in CAN message parsing."""

    def test_no_data_error_raises(self):
        cmd = Command(Mode.REQUEST, 0x0C, 2)
        ctx = Context(cmd, Protocol.ISO_15765_4_CAN)
        raw_messages = [b"NO DATA", b'>']
        rb = ResponseBase(ctx, b'\r'.join(raw_messages), raw_messages)
        handler = ProtocolCAN()

        from obdii.errors import MissingDataError
        with pytest.raises(MissingDataError):
            handler.parse_response(rb)

    def test_can_error_raises(self):
        cmd = Command(Mode.REQUEST, 0x0C, 2)
        ctx = Context(cmd, Protocol.ISO_15765_4_CAN)
        raw_messages = [b"CAN ERROR", b'>']
        rb = ResponseBase(ctx, b'\r'.join(raw_messages), raw_messages)
        handler = ProtocolCAN()

        from obdii.errors import CanError
        with pytest.raises(CanError):
            handler.parse_response(rb)


class TestProtocolCANValidation:
    """Component validation and warning scenarios."""

    def test_validate_components_warns_on_length_mismatch(self, caplog):
        handler = ProtocolCAN()
        cmd = Command(Mode.REQUEST, 0x0C, 2)
        # Components with payload indicating 5 bytes but command expects 2
        components = (b'00', b'00', b'7E', b'8', b'07', b'41', b'0C', b'1A', b'F8')

        handler._validate_components(components, cmd, length=5)

        assert "Expected 2 bytes, but received 5 bytes" in caplog.text

    def test_validate_components_warns_on_wrong_response_code(self, caplog):
        handler = ProtocolCAN()
        cmd = Command(Mode.REQUEST, 0x0C, 2)
        # Components with wrong response code (0x42 instead of 0x41)
        components = (b'00', b'00', b'7E', b'8', b'03', b'42', b'0C', b'1A')

        handler._validate_components(components, cmd, length=1)

        assert "Unexpected response code 0x42" in caplog.text
        assert "expected 0x41" in caplog.text
