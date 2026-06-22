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


class KWPFrame:
    """Minimal representation of a single KWP line as returned by the ELM327.

    Abbreviations:
        ECU = Electronic Control Unit
        FMT = Format
    """

    __slots__ = ("ecu", "payload")

    def __init__(
        self,
        ecu: bytes,
        payload: List[int],
    ) -> None:
        self.ecu = ecu
        self.payload = payload


KWP_PROTOCOLS = {
    Protocol.ISO_9141_2: {},
    Protocol.ISO_14230_4_KWP: {},
    Protocol.ISO_14230_4_KWP_FAST: {},
}


class ProtocolKWP(ProtocolBase, protocols=KWP_PROTOCOLS):
    """Supported Protocols:
    - [0x03] ISO 9141-2 (5 baud init, 10.4 Kbaud)
    - [0x04] ISO 14230-4 KWP (5 baud init, 10.4 Kbaud)
    - [0x05] ISO 14230-4 KWP (fast init, 10.4 Kbaud)

    Required configuration:
    - HEADER_ON
    """

    @staticmethod
    def to_frames(lines: List[bytes], protocol: Protocol) -> List[KWPFrame]:
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
        frames: List[KWPFrame] = []

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

            bytev_len = len(byte_vals)

            if bytev_len < 3:
                _log.warning(f"Line too short to parse: {line!r}")
                continue

            frame = byte_vals[:-1]
            if sum(frame) % 256 != byte_vals[-1]:
                _log.warning(f"Invalid checksum for line: {line!r}")
                continue

            src = byte_vals[2]

            header_len = 3
            if protocol is not Protocol.ISO_9141_2:
                fmt = byte_vals[0]
                if fmt & 0x3F == 0:
                    header_len = 4

            payload = byte_vals[header_len:-1]

            frames.append(
                KWPFrame(
                    f"{src:02X}".encode("ascii"),
                    payload,
                )
            )

        return frames

    @staticmethod
    def to_message(frames: List[KWPFrame], command: Command) -> Optional[List[int]]:
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

        frames = self.to_frames(lines, context.protocol)
        if not frames:
            _log.warning("No valid frames parsed.")
            return Response(**vars(response_base), value=None)

        ecu_frames: Dict[bytes, List[KWPFrame]] = {}
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
