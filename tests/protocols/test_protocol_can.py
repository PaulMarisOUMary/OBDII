"""
Unit tests for obdii.protocols.protocol_can module.

Tests cover both single-frame and multi-frame CAN message parsing per ISO 15765-4.
"""
import pytest

from obdii import commands, at_commands

from obdii.errors import CanError, MissingDataError
from obdii.protocol import Protocol
from obdii.protocols.protocol_can import ProtocolCAN


HANDLER = ProtocolCAN()


class TestProtocolCANSingleFrame:
    """Single-frame CAN message parsing (<=7 data bytes)."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.ISO_15765_4_CAN,
                b"7E8 04 41 0C 40 80\r>",
                [0x40, 0x80],
            ),
            (
                Protocol.ISO_15765_4_CAN_B,
                b"18DAF110 05 41 0C 41 C2\r>",
                [0x41, 0xC2],
            ),
        ],
        ids=["11bit-single-frame", "29bit-single-frame"],
    )
    def test_single_frame_parsing(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, commands.ENGINE_SPEED, protocol, HANDLER)

        assert resp.unparsed == expected


class TestProtocolCANMultiFrame:
    """Multi-frame CAN message parsing (>7 data bytes)."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.ISO_15765_4_CAN,
                b"7E8 10 14 49 02 01 57 56 57\r7E8 21 5A 5A 5A 31 4A 4D 33\r7E8 22 36 33 39 37 36 00 00\r>",
                [0x01, 0x57, 0x56, 0x57, 0x5A, 0x5A, 0x5A, 0x31, 0x4A, 0x4D, 0x33, 0x36, 0x33, 0x39, 0x37, 0x36, 0x00, 0x00],
            ),
            (
                Protocol.ISO_15765_4_CAN_B,
                b"18DAF110 10 14 49 02 01 57 56 57\r18DAF110 21 5A 5A 5A 31 4A 4D 33\r18DAF110 22 36 33 39 37 36 00 00\r>",
                [0x01, 0x57, 0x56, 0x57, 0x5A, 0x5A, 0x5A, 0x31, 0x4A, 0x4D, 0x33, 0x36, 0x33, 0x39, 0x37, 0x36, 0x00, 0x00],
            ),
        ],
        ids=["11bit-multi-frame", "29bit-multi-frame"],
    )
    def test_multi_frame_parsing(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, commands.VIN, protocol, HANDLER)

        assert resp.unparsed == expected


class TestProtocolCANMultiECU:
    """Multi-ECU CAN message parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.ISO_15765_4_CAN,
                b"7E8 04 41 0C 40 80\r7E2 04 41 0C 40 40\r7E9 04 41 0C 40 40\r>",
                {
                    b"7E8": [0x40, 0x80],
                    b"7E2": [0x40, 0x40],
                    b"7E9": [0x40, 0x40],
                },
            ),
            (
                Protocol.ISO_15765_4_CAN_B,
                b"18 DA F1 5A 04 41 0C 0B E8\r18 DA F1 59 04 41 0C 0B E8\r18 DA F1 58 04 41 0C 0B EC\r>",
                {
                    b"18DAF15A": [0x0B, 0xE8],
                    b"18DAF159": [0x0B, 0xE8],
                    b"18DAF158": [0x0B, 0xEC],
                },
            ),
        ],
        ids=["11bit-multi-frame", "29bit-multi-frame"],
    )
    def test_multi_ecu_parsing(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, commands.ENGINE_SPEED, protocol, HANDLER)

        assert resp.messages == expected


class TestProtocolCANATCommands:
    """AT command response parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.ISO_15765_4_CAN,
                b"ELM327 v1.5\r>",
                "ELM327 v1.5"
            ),
        ],
        ids=["atz"],
    )
    def test_at_command_single_line_response(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, at_commands.RESET, protocol, HANDLER)

        assert resp.value == expected


class TestProtocolCANErrors:
    """Error detection and handling in CAN message parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.ISO_15765_4_CAN,
                b"CAN ERROR\r>",
                CanError,
            ),
            (
                Protocol.ISO_15765_4_CAN_B,
                b"NO DATA\r>",
                MissingDataError
            ),
        ],
        ids=["canerror", "nodata"],
    )
    def test_no_data_error_raises(self, protocol_impl, protocol, raw, expected):
        with pytest.raises(expected):
            protocol_impl(raw, commands.ENGINE_SPEED, protocol, HANDLER)