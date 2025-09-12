from logging import getLogger
from typing import List, Tuple

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
    def parse_response(self, response_base: ResponseBase) -> Response:
        context = response_base.context
        command = context.command
        if command.mode == Mode.AT: # AT Commands
            status = None
            if len(response_base.messages[:-1]) == 1:
                status = bytes_to_string(response_base.messages[0])

            return Response(**vars(response_base), value=status)
        else: # OBD Commands
            value = None
            parsed_data: List[Tuple[bytes, ...]] = list()
            for raw_line in response_base.messages[:-1]: # Skip the last line (prompt character)
                line = filter_bytes(raw_line, b' ')

                if not is_bytes_hex(line):
                    is_error = ResponseBaseError.detect(raw_line)
                    if not is_error:
                        continue
                    _log.error(is_error.message)
                    raise is_error

                attr = self.get_protocol_attributes(context.protocol)
                if not "header_length" in attr:
                    raise AttributeError(f"Missing required attribute 'header_length' in protocol attributes for protocol {context.protocol}")

                components = split_hex_bytes(line)

                if attr["header_length"] == 11: # Normalize to 29 bits (32 with hex)
                    components = (b"00",) * 2 + components

                minimal_length = 7 # Less means no data
                if len(components) < minimal_length:
                    _log.warning(f"Invalid line: too few components (expected at least {minimal_length}, got {len(components)})")
                    continue

                # header_end = 4 # unused
                length_idx = 4
                bytes_offset = 2
                response_idx = 5

                # header = b''.join(components[:header_end]) # unused
                length = int(components[length_idx], 16) - bytes_offset
                if length == 0:
                    continue
                response_code = int(components[response_idx], 16)
                data = components[-length:]

                if command.n_bytes and length != command.n_bytes:
                    _log.warning(f"Expected {command.n_bytes} bytes, but received {length} bytes for command {command}")

                if command.mode == Mode.REQUEST and not 0x40 + command.mode.value == response_code:
                    _log.warning(f"Unexpected response code 0x{response_code:02X} for command {command} (expected response code 0x{0x40 + command.mode.value:02X})")

                parsed_data.append(data)
            if command.formula:
                try:
                    value = command.formula(parsed_data)
                except Exception as e:
                    _log.error(f"Unexpected error during formula execution: {e}", exc_info=True)
                    value = None

            return Response(**vars(response_base), parsed_data=parsed_data, value=value)


ProtocolCAN.register({
    Protocol.ISO_15765_4_CAN:   {"header_length": 11},
    Protocol.ISO_15765_4_CAN_B: {"header_length": 29},
    Protocol.ISO_15765_4_CAN_C: {"header_length": 11},
    Protocol.ISO_15765_4_CAN_D: {"header_length" :29},
    Protocol.SAE_J1939_CAN:     {"header_length": 29},
    Protocol.USER1_CAN:         {"header_length": 11}, # 11 bits by default, can be extended
    Protocol.USER2_CAN:         {"header_length": 11}, # 11 bits by default, can be extended
})