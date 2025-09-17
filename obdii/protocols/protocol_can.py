from logging import getLogger
from typing import Any, List, Tuple

from ..basetypes import BytesRows
from ..command import Command
from ..errors import ResponseBaseError
from ..mode import Mode
from ..protocol import Protocol
from ..response import ResponseBase, Response
from ..utils.bits import bytes_to_string, filter_bytes, is_bytes_hex, split_hex_bytes

from .protocol_base import ProtocolBase


_log = getLogger(__name__)


class ProtocolCAN(ProtocolBase):
    """Supported Protocols:
    - [0x06] ISO 15765-4 CAN (11 bit ID, 500 Kbaud)
    - [0x07] ISO 15765-4 CAN (29 bit ID, 500 Kbaud)
    - [0x08] ISO 15765-4 CAN (11 bit ID, 250 Kbaud)
    - [0x09] ISO 15765-4 CAN (29 bit ID, 250 Kbaud)
    - [0x0A] SAE J1939 CAN (29 bit ID, 250 Kbaud)
    - [0x0B] USER1 CAN (11 bit ID, 125 Kbaud)
    - [0x0C] USER2 CAN (11 bit ID, 50 Kbaud)
    """

    _HEADER_LENGTH_11BIT = 11
    _HEADER_LENGTH_29BIT = 29

    _HEADER_BYTES_OFFSET = 2
    _COMPONENTS_MIN_LENGTH = 7
    _IDX_HEADER_END = 4
    _IDX_PAYLOAD_LENGTH = 4
    _IDX_RESPONSE_CODE = 5

    def _strip_prompt(self, messages: List[bytes]) -> List[bytes]:
        return messages[:-1] if messages and messages[-1].strip() == b'>' else messages

    def _normalize_components(
        self, line: bytes, protocol: Protocol
    ) -> Tuple[bytes, ...]:
        attr = self.get_protocol_attributes(protocol)
        header_length = attr.get("header_length")
        if not header_length:
            raise AttributeError(
                f"Missing required attribute 'header_length' in protocol attributes for protocol {protocol}"
            )

        components = split_hex_bytes(line)
        if header_length == self._HEADER_LENGTH_11BIT:
            components = (b"00",) * 2 + components
        return components

    def _validate_components(
        self, components: Tuple[bytes, ...], command: Command, length: int
    ) -> None:
        response_code = int(components[self._IDX_RESPONSE_CODE], 16)

        if command.n_bytes and command.n_bytes != length:
            _log.warning(
                f"Expected {command.n_bytes} bytes, but received {length} bytes for command {command}"
            )
        if command.mode == Mode.REQUEST:
            expected_code = 0x40 + command.mode.value
            if response_code != expected_code:
                _log.warning(
                    f"Unexpected response code 0x{response_code:02X} for command {command} "
                    f"(expected 0x{expected_code:02X})"
                )

    def _parsed_data_to_value(self, command: Command, parsed_data: BytesRows) -> Any:
        value = None
        if command.formula:
            try:
                value = command.formula(parsed_data)
            except Exception as e:
                _log.error(
                    f"Unexpected error during formula execution: {e}", exc_info=True
                )
                value = None
        return value

    def _parse_obd_response(
        self, response_base: ResponseBase, messages: List[bytes]
    ) -> Response:
        context = response_base.context
        command = context.command
        parsed_data: BytesRows = list()

        for raw_line in messages:
            line = filter_bytes(raw_line, b' ')

            if not is_bytes_hex(line):
                is_error = ResponseBaseError.detect(raw_line)
                if is_error:
                    _log.error(is_error.message)
                    raise is_error
                continue

            components = self._normalize_components(line, context.protocol)
            if len(components) < self._COMPONENTS_MIN_LENGTH:
                _log.warning(
                    f"Invalid line: too few components (expected at least {self._COMPONENTS_MIN_LENGTH}, got {len(components)})"
                )
                continue

            # header = b''.join(components[:self._IDX_HEADER_END]) # unused
            payload_length = (
                int(components[self._IDX_PAYLOAD_LENGTH], 16)
                - self._HEADER_BYTES_OFFSET
            )
            if payload_length <= 0:
                continue

            data = components[-payload_length:]
            self._validate_components(components, command, payload_length)
            parsed_data.append(data)

        value = self._parsed_data_to_value(command, parsed_data)
        return Response(**vars(response_base), parsed_data=parsed_data, value=value)

    def _parse_at_response(
        self, response_base: ResponseBase, messages: List[bytes]
    ) -> Response:
        status = None
        if len(messages) == 1:
            status = bytes_to_string(messages[0])
        return Response(**vars(response_base), value=status)

    def parse_response(self, response_base: ResponseBase) -> Response:
        command = response_base.context.command
        messages = self._strip_prompt(response_base.messages)

        if command.mode == Mode.AT:
            return self._parse_at_response(response_base, messages)
        return self._parse_obd_response(response_base, messages)


ProtocolCAN.register(
    {
        Protocol.ISO_15765_4_CAN: {"header_length": 11},
        Protocol.ISO_15765_4_CAN_B: {"header_length": 29},
        Protocol.ISO_15765_4_CAN_C: {"header_length": 11},
        Protocol.ISO_15765_4_CAN_D: {"header_length": 29},
        Protocol.SAE_J1939_CAN: {"header_length": 29},
        Protocol.USER1_CAN: {"header_length": 11},
        Protocol.USER2_CAN: {"header_length": 11},
    }
)
