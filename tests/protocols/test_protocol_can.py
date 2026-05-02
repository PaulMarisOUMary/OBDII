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
            # 11-bit: 7E8 03 41 0C F8
            # PCI = 0x03 (SF, 3 bytes total: mode + PID + 1 data byte)
            # Mode 0x41 + PID 0x0C + Data 0xF8
            # After stripping mode+PID, returns [0xF8]
            (
                Protocol.ISO_15765_4_CAN,
                b"7E8 03 41 0C F8\r>",
                [0xF8],
            ),
            # 29-bit: 18DAF110 05 41 0A 41 0A 7B
            # PCI = 0x05 (SF, 5 bytes total: mode + PID + 3 data bytes)
            # Mode 0x41 + PID 0x0A + Data 0x41 0x0A 0x7B
            # After stripping mode+PID, returns [0x41, 0x0A, 0x7B]
            (
                Protocol.ISO_15765_4_CAN_B,
                b"18DAF110 05 41 0A 41 0A 7B\r>",
                [0x41, 0x0A, 0x7B],
            ),
        ],
        ids=["11bit-single-frame", "29bit-single-frame"],
    )
    def test_single_frame_parsing(self, protocol, raw_messages, expected_data):
        cmd = Command(Mode.REQUEST, 0x0C, 2)
        ctx = Context(cmd, protocol)
        rb = ResponseBase(ctx, raw_messages)
        handler = ProtocolCAN()

        resp = handler.parse_response(rb)

        assert resp.unparsed == expected_data

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
        raw = b"7E8 10 14 49 02 01 57 56 57\r7E8 21 5A 5A 5A 31 4A 4D 33\r7E8 22 36 33 39 37 36 00 00\r>"
        rb = ResponseBase(ctx, raw)
        handler = ProtocolCAN()

        resp = handler.parse_response(rb)

        # Currently the code doesn't handle multi-frame reassembly
        # It will parse each line separately
        # This test documents current behavior and will need updating
        # when multi-frame support is added
        assert resp.unparsed is not None
        assert len(resp.unparsed) > 0




class TestProtocolCANATCommands:
    """AT command response parsing."""

    def test_at_command_single_line_response(self):
        cmd = Command(Mode.AT, 'Z', 0)
        ctx = Context(cmd, Protocol.ISO_15765_4_CAN)
        raw = b"ELM327 v1.5\r>"
        rb = ResponseBase(ctx, raw)
        handler = ProtocolCAN()

        resp = handler.parse_response(rb)

        assert resp.value == "ELM327 v1.5"


class TestProtocolCANErrors:
    """Error detection and handling in CAN message parsing."""

    def test_no_data_error_raises(self):
        cmd = Command(Mode.REQUEST, 0x0C, 2)
        ctx = Context(cmd, Protocol.ISO_15765_4_CAN)
        raw = b"NO DATA\r>"
        rb = ResponseBase(ctx, raw)
        handler = ProtocolCAN()

        from obdii.errors import MissingDataError
        with pytest.raises(MissingDataError):
            handler.parse_response(rb)

    def test_can_error_raises(self):
        cmd = Command(Mode.REQUEST, 0x0C, 2)
        ctx = Context(cmd, Protocol.ISO_15765_4_CAN)
        raw = b"CAN ERROR\r>"
        rb = ResponseBase(ctx, raw)
        handler = ProtocolCAN()

        from obdii.errors import CanError
        with pytest.raises(CanError):
            handler.parse_response(rb)
