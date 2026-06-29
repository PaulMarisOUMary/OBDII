from logging import getLogger
from typing import List, Optional, Dict, Final

from ..command import Command
from ..errors import ResponseBaseError
from ..mode import Mode
from ..protocol import Protocol
from ..response import ResponseBase, Response
from ..utils.bits import filter_bytes

from .protocol_base import ProtocolBase


_log = getLogger(__name__)


class J1850Frame:
    """Minimal representation of a single J1850 line as returned by the ELM327.

    Abbreviations:
        CRC = Cyclic Redundancy Check
        ECU = Electronic Control Unit
        HDR = Header
        IFR = In Frame Response
        SRC = Source
    """

    __slots__ = ("ecu", "payload")

    def __init__(
        self,
        ecu: bytes,
        payload: List[int],
    ) -> None:
        self.ecu = ecu
        self.payload = payload


J1850_PROTOCOLS = {
    Protocol.SAE_J1850_PWM: {},
    Protocol.SAE_J1850_VPW: {},
}


class ProtocolJ1850(ProtocolBase, protocols=J1850_PROTOCOLS):
    """Supported Protocols:
    - [0x01] SAE J1850 PWM (41.6 Kbaud)
    - [0x02] SAE J1850 VPW (10.4 Kbaud)
    """

    EXPECTED_RESIDUE: Final = 0x3B

    @staticmethod
    def compute_crc(frames: List[int]):
        """CRC-8/SAE-J1850"""
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

    @staticmethod
    def to_frames(lines: List[bytes]) -> List[J1850Frame]:
        """
        Parse a list of raw ELM327 lines into J1850Frame objects.

        Frame anatomy and examples
        --------------------------

        - SAE J1850 Frame

        .. code-block:: none

            48 6B 10 41 00 BF DF B9 91 12
            |  |  |  |                 |
            |  |  |  |                 +-- crc: CRC-8/SAE-J1850
            |  |  |  +-- payload: mode (41) + PID (00) + data (BF DF B9 91)
            |  |  +-- source address (sender ECU)
            |  +-- target address (receiver)
            +-- hdr: priority, type, ifr, addressing, message type
        """
        frames: List[J1850Frame] = []

        for raw_lines in lines:
            line = filter_bytes(raw_lines, b' ')
            line_len = len(line)

            if line_len % 2 != 0:
                _log.warning(f"Odd byte count in line: {line!r}")
                continue

            try:
                byte_vals = [int(line[i : i + 2], 16) for i in range(0, line_len, 2)]
            except ValueError:
                continue

            if len(byte_vals) < 5:
                _log.warning(f"Line too short to parse: {line!r}")
                continue

            h_bit = (byte_vals[0] >> 4) & 0x01

            if h_bit == 1:
                _log.warning(f"Invalid header type for line: {line!r}")
                continue

            residue = ProtocolJ1850.compute_crc(byte_vals)
            if residue != ProtocolJ1850.EXPECTED_RESIDUE:
                _log.warning(
                    f"Invalid Cyclic Redundancy Check ({residue:02X}) for line: {line!r}"
                )
                continue

            src = byte_vals[2]
            ecu = f"{src:02X}".encode("ascii")

            payload = byte_vals[3:-1]

            frames.append(
                J1850Frame(
                    ecu,
                    payload,
                )
            )

        return frames

    @staticmethod
    def to_message(frames: List[J1850Frame], command: Command) -> Optional[List[int]]:
        strip = 2 if command.pid != '' else 1

        if len(frames) == 1:
            payload = frames[0].payload
            if len(payload) < strip:
                _log.warning("Single Frame payload too short to strip mode + pid")
                return None
            return payload[strip:]

        seq_index = strip

        sorted_frames = sorted(
            frames,
            key=lambda f: f.payload[seq_index] if len(f.payload) > seq_index else 0,
        )

        data_start = seq_index + 1
        message = []
        for frame in sorted_frames:
            payload = frame.payload
            if len(payload) <= data_start:
                continue
            message.extend(payload[data_start:])

        return message

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

        frames = self.to_frames(lines)
        if not frames:
            _log.warning("No valid frames parsed.")
            return Response(**vars(response_base), value=None)

        ecu_frames: Dict[bytes, List[J1850Frame]] = {}
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
