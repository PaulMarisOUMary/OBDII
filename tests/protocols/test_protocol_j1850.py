"""
Unit tests for obdii.protocols.protocol_j1850 module.

Tests cover both single-frame and multi-frame message parsing
for SAE J1850 PWM and SAE J1850 VPW.
"""
import pytest

from obdii import commands, at_commands

from obdii.errors import BusBusyError, BusError, MissingDataError
from obdii.protocol import Protocol
from obdii.protocols.protocol_j1850 import ProtocolJ1850


HANDLER = ProtocolJ1850()


class TestProtocolJ1850SingleFrame:
    """Single-frame J1850 message parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.SAE_J1850_PWM,
                b"48 6B 10 41 0C 0D 48 93\r>",
                [0x0D, 0x48],
            ),
            (
                Protocol.SAE_J1850_VPW,
                b"48 6B 10 41 0C 27 10 12\r>",
                [0x27, 0x10],
            ),
            (
                Protocol.SAE_J1850_PWM,
                b"48 6B 10 41 0D 00 CA\r>",
                [0x00],
            ),
            (
                Protocol.SAE_J1850_VPW,
                b"48 6B 10 41 0D 50 14\r>",
                [0x50],
            ),
        ],
        ids=["pwm-engine-speed", "vpw-engine-speed", "pwm-vehicle-speed", "vpw-vehicle-speed"],
    )
    def test_single_frame_parsing(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, commands.ENGINE_SPEED, protocol, HANDLER)

        assert resp.unparsed == expected


class TestProtocolJ1850MultiFrame:
    """Multi-frame J1850 message parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.SAE_J1850_PWM,
                (
                    b"48 6B 10 49 02 01 31 47 31 4A 43 49 \r"
                    b"48 6B 10 49 02 02 35 34 34 34 52 37 42 \r"
                    b"48 6B 10 49 02 03 32 35 33 36 37 D5 \r"
                    b">"
                ),
                [0x31, 0x47, 0x31, 0x4A, 0x43, 0x35, 0x34, 0x34, 0x34, 0x52, 0x37, 0x32, 0x35, 0x33, 0x36, 0x37],
            ),
            (
                Protocol.SAE_J1850_VPW,
                (
                    b"48 6B 10 49 02 01 31 47 31 4A 43 49 \r"
                    b"48 6B 10 49 02 02 35 34 34 34 52 37 42 \r"
                    b"48 6B 10 49 02 03 32 35 33 36 37 D5 \r"
                    b">"
                ),
                [0x31, 0x47, 0x31, 0x4A, 0x43, 0x35, 0x34, 0x34, 0x34, 0x52, 0x37, 0x32, 0x35, 0x33, 0x36, 0x37],
            ),
        ],
        ids=["pwm-vin", "vpw-vin"],
    )
    def test_multi_frame_parsing(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, commands.VIN, protocol, HANDLER)

        assert resp.unparsed == expected


class TestProtocolJ1850MultiECU:
    """Multi-ECU J1850 message parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.SAE_J1850_PWM,
                b"48 6B 10 41 0C 0D 48 93\r48 6B 18 41 0C 0F A0 26\r>",
                {
                    b"10": [0x0D, 0x48],
                    b"18": [0x0F, 0xA0],
                },
            ),
            (
                Protocol.SAE_J1850_VPW,
                b"48 6B 10 41 0C 27 10 12\r48 6B 18 41 0C 0F A0 26\r>",
                {
                    b"10": [0x27, 0x10],
                    b"18": [0x0F, 0xA0],
                },
            ),
        ],
        ids=["pwm-multi-ecu", "vpw-multi-ecu"],
    )
    def test_multi_ecu_parsing(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, commands.ENGINE_SPEED, protocol, HANDLER)

        assert resp.messages == expected


class TestProtocolJ1850ATCommands:
    """AT command response parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.SAE_J1850_PWM,
                b"ELM327 v1.5\r>",
                "ELM327 v1.5",
            ),
            (
                Protocol.SAE_J1850_VPW,
                b"ELM327 v1.5\r>",
                "ELM327 v1.5",
            ),
        ],
        ids=["pwm-atz", "vpw-atz"],
    )
    def test_at_command_single_line_response(self, protocol_impl, protocol, raw, expected):
        resp = protocol_impl(raw, at_commands.RESET, protocol, HANDLER)

        assert resp.value == expected


class TestProtocolJ1850Errors:
    """Error detection and handling in J1850 message parsing."""

    @pytest.mark.parametrize(
        ("protocol", "raw", "expected"),
        [
            (
                Protocol.SAE_J1850_PWM,
                b"BUS BUSY\r>",
                BusBusyError,
            ),
            (
                Protocol.SAE_J1850_VPW,
                b"NO DATA\r>",
                MissingDataError,
            ),
            (
                Protocol.SAE_J1850_PWM,
                b"BUS ERROR\r>",
                BusError,
            ),
        ],
        ids=["pwm-busbusy", "vpw-nodata", "pwm-buserror"],
    )
    def test_error_raises(self, protocol_impl, protocol, raw, expected):
        with pytest.raises(expected):
            protocol_impl(raw, commands.ENGINE_SPEED, protocol, HANDLER)