from enum import IntEnum
from logging import getLogger
from typing import List, Optional, Dict

from ..command import Command
from ..errors import ResponseBaseError
from ..mode import Mode
from ..protocol import Protocol
from ..response import ResponseBase, Response
from ..utils.bits import filter_bytes

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


class CANFrame:
    """Minimal representation of a single CAN line as returned by the ELM327.

    Abbreviations:
        ECU = Electronic Control Unit
        SN = Sequence Number
        DLC = Data Length Code
    """

    __slots__ = ("ecu", "kind", "sn", "dlc", "payload")

    def __init__(
        self,
        ecu: bytes,
        kind: FrameKind,
        payload: List[int],
        sn: int = 0,
        dlc: int = 0,
    ) -> None:
        self.ecu = ecu
        self.kind = kind
        self.sn = sn
        self.dlc = dlc
        self.payload = payload


CAN_PROTOCOLS = {
    Protocol.ISO_15765_4_CAN: {"header_length": 11},
    Protocol.ISO_15765_4_CAN_B: {"header_length": 29},
    Protocol.ISO_15765_4_CAN_C: {"header_length": 11},
    Protocol.ISO_15765_4_CAN_D: {"header_length": 29},
    Protocol.SAE_J1939_CAN: {"header_length": 29},
    Protocol.USER1_CAN: {"header_length": 11},
    Protocol.USER2_CAN: {"header_length": 11},
}


class ProtocolCAN(ProtocolBase, protocols=CAN_PROTOCOLS):
    """Supported Protocols:
    - [0x06] ISO 15765-4 CAN (11 bit ID, 500 Kbaud)
    - [0x07] ISO 15765-4 CAN (29 bit ID, 500 Kbaud)
    - [0x08] ISO 15765-4 CAN (11 bit ID, 250 Kbaud)
    - [0x09] ISO 15765-4 CAN (29 bit ID, 250 Kbaud)
    - [0x0A] SAE J1939 CAN (29 bit ID, 250 Kbaud)
    - [0x0B] USER1 CAN (11 bit ID, 125 Kbaud)
    - [0x0C] USER2 CAN (11 bit ID, 50 Kbaud)
    """

    @staticmethod
    def to_lines(raw: bytes) -> List[bytes]:
        return [
            line for line in raw.splitlines() if line.strip() and line.strip() != b'>'
        ]

    @staticmethod
    def to_frames(lines: List[bytes], header_len: int) -> List[CANFrame]:
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
        frames: List[CANFrame] = []
        header_chars = (header_len + 3) // 4

        for raw_line in lines:
            line = filter_bytes(raw_line, b' ')

            if len(line) < header_chars + 4:
                _log.warning(f"Line too short to parse: {line!r}")
                continue

            ecu = line[:header_chars]
            rest = line[header_chars:]

            rest_len = len(rest)
            if rest_len % 2 != 0:
                _log.warning(f"Odd byte count after header in line {line!r}")
                continue

            try:
                byte_vals = [int(rest[i : i + 2], 16) for i in range(0, len(rest), 2)]
            except ValueError:
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

    @staticmethod
    def to_message(frames: List[CANFrame], command: Command) -> Optional[List[int]]:
        strip = 2 if command.pid != '' else 1

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

    def parse_response(self, response_base: ResponseBase) -> Response:
        context = response_base.context
        raw = response_base.raw

        mode = Mode.get_from(context.command.mode)
        if mode is Mode.AT:
            value = "\n".join(
                [line.decode(errors="ignore").strip() for line in self.to_lines(raw)]
            )
            return Response(**vars(response_base), value=value)

        error = ResponseBaseError.detect(raw)
        if error:
            _log.error(error.message)
            raise error

        lines = self.to_lines(raw)
        if not lines:
            _log.warning("Empty response.")
            return Response(**vars(response_base), value=None)

        attr = self.get_protocol_attributes(context.protocol)
        header_len = attr["header_length"]

        frames = self.to_frames(lines, header_len)
        if not frames:
            _log.warning("No valid frames parsed.")
            return Response(**vars(response_base), value=None)

        ecu_frames: Dict[bytes, List[CANFrame]] = {}
        for frame in frames:
            ecu_frames.setdefault(frame.ecu, []).append(frame)

        message = None
        ecu_messages: Dict[bytes, List[int]] = {}
        for ecu, frames_list in ecu_frames.items():
            _message = self.to_message(frames_list, context.command)
            if _message is not None:
                ecu_messages[ecu] = _message
                if message is None:
                    message = _message

        if not ecu_messages:
            _log.warning("No message could be reassembled.")

        value = None
        resolver = context.command.resolver

        if resolver:
            try:
                value = resolver(message)
            except Exception as e:
                _log.error(
                    f"Unexpected error during formula execution: {e}", exc_info=True
                )
                value = None

        return Response(
            **vars(response_base), unparsed=message, messages=ecu_messages, value=value
        )
