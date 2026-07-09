from logging import getLogger
from typing import List, Final

from ..protocol import Protocol
from ..response import Context
from ..utils.bits import filter_bytes, to_bytes

from .protocol_base import ProtocolBase
from .mixins import Frame, J1979Mixin, ParsingMixin


_log = getLogger(__name__)


J1850_PROTOCOLS = {
    Protocol.SAE_J1850_PWM: {},
    Protocol.SAE_J1850_VPW: {},
}


class ProtocolJ1850(ParsingMixin, J1979Mixin, ProtocolBase, protocols=J1850_PROTOCOLS):
    """Supported Protocols:
    - [0x01] SAE J1850 PWM (41.6 Kbaud)
    - [0x02] SAE J1850 VPW (10.4 Kbaud)

    Required configuration:
    - HEADER_ON
    """

    EXPECTED_RESIDUE: Final = 0x3B
    """:meta private:"""

    def compute_crc(self, frames: List[int]):
        """:meta private:
        CRC-8/SAE-J1850"""
        crc = 0xFF
        poly = 0x1D

        for byte in frames:
            crc ^= byte & 0xFF
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
                crc &= 0xFF
        return crc ^ 0xFF

    def to_frames(self, lines: List[bytes], context: Context) -> List[Frame]:
        """
        Parse a list of raw ELM327 lines into J1850Frame objects.

        Frame anatomy and examples
        --------------------------

        SAE J1850 Frame

        .. code-block:: none

            48 6B 10 41 00 BF DF B9 91 12
            |  |  |  |                 |
            |  |  |  |                 +-- crc: CRC-8/SAE-J1850
            |  |  |  +-- payload: mode (41) + PID (00) + data (BF DF B9 91)
            |  |  +-- source address (sender ECU)
            |  +-- target address (receiver)
            +-- hdr: priority, type, ifr, addressing, message type
        """
        frames: List[Frame] = []

        for raw_lines in lines:
            line = filter_bytes(raw_lines, b' ')

            try:
                byte_vals = to_bytes(line)
            except ValueError as e:
                _log.warning(f"Invalid hex payload in line: {line!r}: {e}")
                continue

            if len(byte_vals) < 5:
                _log.warning(f"Line too short to parse: {line!r}")
                continue

            h_bit = (byte_vals[0] >> 4) & 0x01

            if h_bit == 1:
                _log.warning(f"Invalid header type for line: {line!r}")
                continue

            residue = self.compute_crc(byte_vals)
            if residue != self.EXPECTED_RESIDUE:
                _log.warning(
                    f"Invalid Cyclic Redundancy Check ({residue:02X}) for line: {line!r}"
                )
                continue

            src = byte_vals[2]
            ecu = f"{src:02X}".encode("ascii")

            payload = byte_vals[3:-1]

            frames.append(
                Frame(
                    ecu,
                    payload,
                )
            )

        return frames
