from enum import IntEnum
from logging import getLogger
from typing import List, Optional, Union, cast

from ..protocol import Protocol
from ..response import Context
from ..utils.bits import filter_bytes, hex_byte_length, hex_to_ints
from .mixins import Frame, ParsingMixin
from .protocol_base import ProtocolBase

_log = getLogger(__name__)


class FrameKind(IntEnum):
    """
    Abbreviations:
        SF = Single Frame
        FF = First Frame
        CF = Consecutive Frame
        FC = Flow Control Frame
    """

    SINGLE = 0x00
    FIRST = 0x10
    CONSECUTIVE = 0x20


class CANFrame(Frame):
    """Minimal representation of a single CAN line as returned by the ELM327.

    Abbreviations:
        SN = Sequence Number
        DLC = Data Length Code
    """

    __slots__ = ("dlc", "kind", "sn")

    def __init__(
        self,
        ecu: bytes,
        kind: FrameKind,
        payload: List[int],
        sn: int = 0,
        dlc: int = 0,
    ) -> None:
        super().__init__(ecu, payload)
        self.kind = kind
        self.sn = sn
        self.dlc = dlc


CAN_PROTOCOLS = {
    Protocol.ISO_15765_4_CAN: {"header_length": 11},
    Protocol.ISO_15765_4_CAN_B: {"header_length": 29},
    Protocol.ISO_15765_4_CAN_C: {"header_length": 11},
    Protocol.ISO_15765_4_CAN_D: {"header_length": 29},
    Protocol.SAE_J1939_CAN: {"header_length": 29},
    Protocol.USER1_CAN: {"header_length": 11},
    Protocol.USER2_CAN: {"header_length": 11},
}


class ProtocolCAN(ParsingMixin[CANFrame], ProtocolBase, protocols=CAN_PROTOCOLS):
    """Supported Protocols:
    - [0x06] ISO 15765-4 CAN (11 bit ID, 500 Kbaud)
    - [0x07] ISO 15765-4 CAN (29 bit ID, 500 Kbaud)
    - [0x08] ISO 15765-4 CAN (11 bit ID, 250 Kbaud)
    - [0x09] ISO 15765-4 CAN (29 bit ID, 250 Kbaud)
    - [0x0A] SAE J1939 CAN (29 bit ID, 250 Kbaud)
    - [0x0B] USER1 CAN (11 bit ID, 125 Kbaud)
    - [0x0C] USER2 CAN (11 bit ID, 50 Kbaud)

    Required configuration:
    - HEADER_ON
    """

    def to_frames(self, lines: List[bytes], context: Context) -> List[CANFrame]:
        """
        Parse a list of raw ELM327 lines into CANFrame objects.

        Frame anatomy and examples
        --------------------------

        Single Frame (SF) - complete message in one line

        .. code-block:: none

            7E8 04 41 0C 41 C2
            |   |  |
            |   |  +-- payload: mode (41) + PID (0C) + data (41 C2)
            |   +-- PCI: high nibble 0x0 = SF, low nibble 0x4 = DLC (4 bytes)
            +-- ECU address (11-bit)

        First Frame (FF) - first frame of a multi-frame message

        .. code-block:: none

            7E8 10 14 49 02 01 57 50 30
            |   |  |  |
            |   |  |  +-- payload start: mode (49) + PID (02) + data (57 50 30)
            |   |  +-- DLC low byte: 0x14 = 20 -> DLC(20 bytes)
            |   +-- PCI: high nibble 0x1 = FF, low nibble 0x0 = DLC high bits
            +-- ECU address (11-bit)

        Consecutive Frame (CF) - continuation of a multi-frame message

        .. code-block:: none

            7E8 21 5A 5A 5A 39 39 5A 54
            |   |  |
            |   |  +-- payload continuation (no mode, no PID, only data)
            |   +-- PCI: high nibble 0x2 = CF, low nibble 0x1 = SN
            +-- ECU address (11-bit)
        """
        attr = self.get_protocol_attributes(context.protocol)
        header_len = attr["header_length"]

        frames: List[CANFrame] = []
        header_chars = (header_len + 3) // 4

        for raw_line in lines:
            line = filter_bytes(raw_line, b' ')

            if len(line) < header_chars + 4:
                _log.warning(f"Line too short to parse: {line!r}")
                continue

            ecu = line[:header_chars]
            rest = line[header_chars:]

            try:
                byte_vals = hex_to_ints(rest)
            except ValueError as e:
                _log.warning(f"Invalid hex payload in line: {line!r}: {e}")
                continue

            if not byte_vals:
                _log.warning(f"No bytes after header in line: {line!r}")
                continue

            pci = byte_vals[0]
            kind = pci & 0xF0

            if kind == FrameKind.SINGLE:
                dlc = pci & 0x0F
                payload = byte_vals[1 : 1 + dlc]

                frame = CANFrame(
                    ecu=ecu, kind=FrameKind.SINGLE, dlc=dlc, payload=payload
                )
            elif kind == FrameKind.FIRST:
                dlc = ((pci & 0x0F) << 8) | byte_vals[1]
                payload = byte_vals[2:]

                frame = CANFrame(
                    ecu=ecu, kind=FrameKind.FIRST, dlc=dlc, payload=payload
                )

            elif kind == FrameKind.CONSECUTIVE:
                sn = pci & 0x0F
                payload = byte_vals[1:]

                frame = CANFrame(
                    ecu=ecu, kind=FrameKind.CONSECUTIVE, sn=sn, payload=payload
                )
            else:
                _log.warning(f"Unknown frame kind in line: {line!r}")
                continue

            frames.append(frame)

        return frames

    def to_message(
        self, frames: List[CANFrame], context: Context
    ) -> Optional[List[int]]:
        pid = cast(Union[str, int], context.command.pid)
        strip = 1 + hex_byte_length(pid)

        if len(frames) == 1 and frames[0].kind == FrameKind.SINGLE:
            payload = frames[0].payload
            if len(payload) < strip:
                _log.warning("Single Frame payload too short to strip mode + pid")
                return None
            return payload[strip:]

        first_frames = [f for f in frames if f.kind == FrameKind.FIRST]
        consecutives = [f for f in frames if f.kind == FrameKind.CONSECUTIVE]

        if not first_frames:
            _log.warning("No First Frame found.")
            return None

        if len(first_frames) > 1:
            _log.warning("Multiple First Frames detected.")
            return None

        first = first_frames[0]
        dlc = first.dlc

        consecutives.sort(key=lambda f: f.sn)

        message = first.payload.copy()
        for cf in consecutives:
            message.extend(cf.payload)

        if len(message) != dlc:
            _log.warning(f"Incomplete message: expected {dlc}, got {len(message)}")
            return None

        return message[strip:]
