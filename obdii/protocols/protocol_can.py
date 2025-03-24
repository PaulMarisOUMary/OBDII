from logging import getLogger
from typing import List, Tuple

from ..basetypes import BaseResponse, Context, Mode, Protocol, Response
from ..protocol import BaseProtocol
from ..utils import bytes_to_string, filter_bytes, is_bytes_hexadecimal, split_by_byte


_log = getLogger(__name__)


class ProtocolCAN(BaseProtocol):
    """Supported Protocols:
    - [0x06] ISO 15765-4 CAN (11 bit ID, 500 Kbaud)
    - [0x07] ISO 15765-4 CAN (29 bit ID, 500 Kbaud)
    - [0x08] ISO 15765-4 CAN (11 bit ID, 250 Kbaud)
    - [0x09] ISO 15765-4 CAN (29 bit ID, 250 Kbaud)
    - [0x0A] SAE J1939 CAN (29 bit ID, 250 Kbaud)
    - [0x0B] USER1 CAN (11 bit ID, 125 Kbaud)
    - [0x0C] USER2 CAN (11 bit ID, 50 Kbaud)
    """
    def parse_response(self, base_response: BaseResponse, context: Context) -> Response:
        command = context.command
        if command.mode == Mode.AT: # AT Commands
            status = None
            if len(base_response.message[:-1]) == 1:
                status = bytes_to_string(base_response.message[0])

            return Response(**base_response.__dict__, value=status)
        else: # OBD Commands
            value = None
            parsed_data: List[Tuple[bytes, ...]] = list()
            for raw_line in base_response.message[:-1]: # Skip the last line (prompt character)
                line = filter_bytes(raw_line, b' ')

                if not is_bytes_hexadecimal(line):
                    # if pattern match our_errors
                    # _log.error("Check for errors.py Soon TM")
                    continue # code error handling

                attr = self.get_protocol_attributes(context.protocol)
                if not "header_length" in attr:
                    raise AttributeError(f"Missing required attribute 'header_length' in protocol attributes for protocol {context.protocol}")

                components = split_by_byte(line)

                if attr["header_length"] == 11: # Normalize to 29 bits (32 with hex)
                    components = (b"00",) * 2 + components

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

            return Response(**base_response.__dict__, parsed_data=parsed_data, value=value)


ProtocolCAN.register({
    Protocol.ISO_15765_4_CAN:   {"header_length": 11},
    Protocol.ISO_15765_4_CAN_B: {"header_length": 29},
    Protocol.ISO_15765_4_CAN_C: {"header_length": 11},
    Protocol.ISO_15765_4_CAN_D: {"header_length" :29},
    Protocol.SAE_J1939_CAN:     {"header_length": 29},
    Protocol.USER1_CAN:         {"header_length": 11}, # 11 bits by default
    Protocol.USER2_CAN:         {"header_length": 11},
})