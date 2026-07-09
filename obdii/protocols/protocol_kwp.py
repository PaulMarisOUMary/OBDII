from logging import getLogger
from typing import List

from ..protocol import Protocol
from ..response import Context
from ..utils.bits import filter_bytes, to_bytes

from .protocol_base import ProtocolBase
from .mixins import Frame, J1979Mixin, ParsingMixin


_log = getLogger(__name__)


KWP_PROTOCOLS = {
    Protocol.ISO_9141_2: {},
    Protocol.ISO_14230_4_KWP: {},
    Protocol.ISO_14230_4_KWP_FAST: {},
}


class ProtocolKWP(ParsingMixin, J1979Mixin, ProtocolBase, protocols=KWP_PROTOCOLS):
    """Supported Protocols:
    - [0x03] ISO 9141-2 (5 baud init, 10.4 Kbaud)
    - [0x04] ISO 14230-4 KWP (5 baud init, 10.4 Kbaud)
    - [0x05] ISO 14230-4 KWP (fast init, 10.4 Kbaud)

    Required configuration:
    - HEADER_ON
    """

    def to_frames(self, lines: List[bytes], context: Context) -> List[Frame]:
        """
        Parse a list of raw ELM327 lines into KWPFrame objects.

        Frame anatomy and examples
        --------------------------

        ISO 9141-2 Frame - fixed 3 byte header

        .. code-block:: none

            48 6B 11 41 0C 1F 40 70
            |  |  |  |           |
            |  |  |  |           +-- checksum: sum of all previous bytes % 256
            |  |  |  +-- payload: mode (41) + PID (0C) + data (1F 40)
            |  |  +-- source address (sender ECU)
            |  +-- target address (receiver)
            +-- priority

        ISO 14230-4 Frame (Standard Header) - length inline within FMT byte

        .. code-block:: none

            84 F1 11 41 0C 1F 44 36
            |  |  |  |           |
            |  |  |  |           +-- checksum: sum of all previous bytes % 256
            |  |  |  +-- payload: mode (41) + PID (0C) + data (1F 44)
            |  |  +-- source address (sender ECU)
            |  +-- target address (receiver)
            +-- FMT: addressing mode (bits 7:6) + payload length (bits 5:0 = 4 bytes)

        ISO 14230-4 Frame (Extended Header) - length in a separate LEN byte

        .. code-block:: none

            80 F1 11 04 41 0C 1F 44 32
            |  |  |  |  |           |
            |  |  |  |  |           +-- checksum: sum of all previous bytes % 256
            |  |  |  |  +-- payload: mode (41) + PID (0C) + data (1F 44)
            |  |  |  +-- LEN: payload length byte (present because bits 5:0 of FMT = 0)
            |  |  +-- source address (sender ECU)
            |  +-- target address (receiver)
            +-- FMT: addressing mode (bits 7:6) + length flag (bits 5:0 = 0)
        """
        protocol = context.protocol
        frames: List[Frame] = []

        for raw_lines in lines:
            line = filter_bytes(raw_lines, b' ')

            try:
                byte_vals = to_bytes(line)
            except ValueError as e:
                _log.warning(f"Invalid hex payload in line: {line!r}: {e}")
                continue

            bytev_len = len(byte_vals)

            if bytev_len < 3:
                _log.warning(f"Line too short to parse: {line!r}")
                continue

            frame = byte_vals[:-1]
            if sum(frame) % 256 != byte_vals[-1]:
                _log.warning(f"Invalid checksum for line: {line!r}")
                continue

            src = byte_vals[2]
            ecu = f"{src:02X}".encode("ascii")

            header_len = 3
            if protocol is not Protocol.ISO_9141_2:
                fmt = byte_vals[0]
                if fmt & 0x3F == 0:
                    header_len = 4

            payload = byte_vals[header_len:-1]

            frames.append(
                Frame(
                    ecu,
                    payload,
                )
            )

        return frames
