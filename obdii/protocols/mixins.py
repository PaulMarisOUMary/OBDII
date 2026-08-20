from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, Generic, List, Optional, TypeVar, Union, cast

from ..errors import ResponseBaseError
from ..mode import Mode
from ..response import Context, Response, ResponseBase
from ..utils.bits import hex_byte_length

_log = getLogger(__name__)


class Frame:
    """Minimal representation of a single parsed line, common to every protocol family.

    Abbreviations:
        ECU = Electronic Control Unit
    """

    __slots__ = ("ecu", "payload")

    def __init__(self, ecu: bytes, payload: List[int]) -> None:
        self.ecu = ecu
        self.payload = payload


FrameT = TypeVar("FrameT", bound=Frame)


class ParsingABC(ABC, Generic[FrameT]):
    @abstractmethod
    def to_frames(self, lines: List[bytes], context: Context) -> List[FrameT]: ...

    @abstractmethod
    def to_message(
        self, frames: List[FrameT], context: Context
    ) -> Optional[List[int]]: ...


class ParsingMixin(ParsingABC[FrameT], Generic[FrameT]):
    def to_lines(self, raw: bytes) -> List[bytes]:
        return [
            line for line in raw.splitlines() if line.strip() and line.strip() != b'>'
        ]

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

        frames = self.to_frames(lines, context)
        if not frames:
            _log.warning("No valid frames parsed.")
            return Response(**vars(response_base), value=None)

        ecu_frames: Dict[bytes, List[FrameT]] = {}
        for frame in frames:
            ecu_frames.setdefault(frame.ecu, []).append(frame)

        message = None
        ecu_messages: Dict[bytes, List[int]] = {}
        for ecu, frames_list in ecu_frames.items():
            _message = self.to_message(frames_list, context)
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


class J1979Mixin(ParsingABC):
    def to_message(self, frames: List[Frame], context: Context) -> Optional[List[int]]:
        pid = cast(Union[str, int], context.command.pid)
        strip = 1 + hex_byte_length(pid)

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
