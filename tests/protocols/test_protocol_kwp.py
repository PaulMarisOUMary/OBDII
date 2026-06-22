"""
Unit tests for obdii.protocols.protocol_kwp module.

Tests cover both single-frame and multi-frame message parsing per ISO 9141-2 and ISO 14230-4.
"""
import pytest

from obdii import commands, at_commands

from obdii.errors import BusBusyError, BusError, MissingDataError
from obdii.protocol import Protocol
from obdii.protocols.protocol_kwp import ProtocolKWP


HANDLER = ProtocolKWP()


class TestProtocolKWPSingleFrame:
    """Single-frame KWP message parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.ISO_9141_2,
                b"48 6B 11 41 0C 1F 40 70\r>",
                [0x1F, 0x40],
            ),
            (
                Protocol.ISO_14230_4_KWP,
                b"84 F1 11 41 0C 1F 44 36\r>",
                [0x1F, 0x44],
            ),
            (
                Protocol.ISO_14230_4_KWP_FAST,
                b"84 F1 11 41 0C 1F 44 36\r>",
                [0x1F, 0x44],
            ),
        ],
        ids=["iso-9141-2", "iso-14230-4", "iso-14230-4-fast"],
    )
    def test_single_frame_parsing(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, commands.ENGINE_SPEED, protocol, HANDLER)

        assert resp.unparsed == expected


class TestProtocolKWPMultiFrame:
    """Multi-frame KWP message parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.ISO_9141_2,
                b"48 6B 11 49 02 01 00 00 00 31 41 \r48 6B 11 49 02 02 41 31 4A 43 10 \r48 6B 11 49 02 03 35 34 34 34 E3 \r48 6B 11 49 02 04 52 37 32 35 03 \r48 6B 11 49 02 05 32 33 36 37 E6 \r>",
                [0x00, 0x00, 0x00, 0x31, 0x41, 0x31, 0x4A, 0x43, 0x35, 0x34, 0x34, 0x34, 0x52, 0x37, 0x32, 0x35, 0x32, 0x33, 0x36, 0x37],
            ),
            (
                Protocol.ISO_14230_4_KWP,
                b"87 F1 11 49 02 01 00 00 00 31 06 \r87 F1 11 49 02 02 41 31 4A 43 D5 \r87 F1 11 49 02 03 35 34 34 34 A8\r87 F1 11 49 02 04 52 37 32 35 C8\r>",
                [0x00, 0x00, 0x00, 0x31, 0x41, 0x31, 0x4A, 0x43, 0x35, 0x34, 0x34, 0x34, 0x52, 0x37, 0x32, 0x35],
            ),
            (
                Protocol.ISO_14230_4_KWP_FAST,
                b"87 F1 11 49 02 01 00 00 00 31 06 \r87 F1 11 49 02 02 41 31 4A 43 D5 \r87 F1 11 49 02 03 35 34 34 34 A8\r87 F1 11 49 02 04 52 37 32 35 C8\r>",
                [0x00, 0x00, 0x00, 0x31, 0x41, 0x31, 0x4A, 0x43, 0x35, 0x34, 0x34, 0x34, 0x52, 0x37, 0x32, 0x35],
            ),
        ],
        ids=["iso-9141-2", "iso-14230-4", "iso-14230-4-fast"],
    )
    def test_multi_frame_parsing(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, commands.VIN, protocol, HANDLER)

        assert resp.unparsed == expected


class TestProtocolKWPMultiECU:
    """Multi-ECU KWP message parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.ISO_9141_2,
                b"48 6B 11 41 0C 1F 40 70\r48 6B 12 41 0C 0F A0 C1\r>",
                {
                    b"11": [0x1F, 0x40],
                    b"12": [0x0F, 0xA0],
                },
            ),
            (
                Protocol.ISO_14230_4_KWP,
                b"84 F1 11 41 0C 1F 44 36\r84 F1 12 41 0C 0F A0 83\r>",
                {
                    b"11": [0x1F, 0x44],
                    b"12": [0x0F, 0xA0],
                },
            ),
            (
                Protocol.ISO_14230_4_KWP_FAST,
                b"84 F1 11 41 0C 1F 44 36\r84 F1 12 41 0C 0F A0 83\r>",
                {
                    b"11": [0x1F, 0x44],
                    b"12": [0x0F, 0xA0],
                },
            ),
        ],
        ids=["iso-9141-2", "iso-14230-4", "iso-14230-4-fast"],
    )
    def test_multi_ecu_parsing(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, commands.ENGINE_SPEED, protocol, HANDLER)

        assert resp.messages == expected


class TestProtocolKWPATCommands:
    """AT command response parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.ISO_9141_2,
                b"ELM327 v1.5\r>",
                "ELM327 v1.5"
            ),
        ],
        ids=["atz"],
    )
    def test_at_command_single_line_response(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, at_commands.RESET, protocol, HANDLER)

        assert resp.value == expected


class TestProtocolKWPErrors:
    """Error detection and handling in KWP message parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.ISO_9141_2,
                b"BUS BUSY\r>",
                BusBusyError,
            ),
            (
                Protocol.ISO_14230_4_KWP,
                b"NO DATA\r>",
                MissingDataError
            ),
            (
                Protocol.ISO_14230_4_KWP_FAST,
                b"BUS ERROR\r>",
                BusError
            ),
        ],
        ids=["busbusy", "nodata", "buserror"],
    )
    def test_no_data_error_raises(self, protocol_impl, protocol, raw, expected):
        with pytest.raises(expected):
            protocol_impl(raw, commands.ENGINE_SPEED, protocol, HANDLER)