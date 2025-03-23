from logging import getLogger
from typing import List

from ..basetypes import BaseResponse, Command, Mode, Protocol, Response
from ..protocol import BaseProtocol
from ..utils import bytes_to_string, filter_bytes, is_bytes_hexadecimal


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
    def parse_response(self, base_response: BaseResponse, command: Command) -> Response:
        if command.mode == Mode.AT: # AT Commands
            status = None
            if len(base_response.message[:-1]) == 1:
                status = bytes_to_string(base_response.message[0])

            return Response(**base_response.__dict__, value=status)
        else: # OBD Commands
            value = None
            parsed_data = list()
            for raw_line in base_response.message[:-1]: # Skip the last line (prompt character)
                line = filter_bytes(raw_line, b' ')


                if not is_bytes_hexadecimal(line):
                    continue # code error handling






            if command.formula:
                try:
                    value = command.formula(parsed_data)
                except Exception:
                    value = None

            return Response(**base_response.__dict__, parsed_data=parsed_data, value=value)


ProtocolCAN.register(
    Protocol.ISO_15765_4_CAN, Protocol.ISO_15765_4_CAN_B, Protocol.ISO_15765_4_CAN_C,
    Protocol.ISO_15765_4_CAN_D, Protocol.SAE_J1939_CAN, Protocol.USER1_CAN, Protocol.USER2_CAN
)