from logging import getLogger

from ..basetypes import BaseResponse, Command, Mode, Protocol, Response
from ..protocol import BaseProtocol
from ..utils import bytes_to_string, is_hexadecimal, split_by_bytes


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
                status = ''.join([c.decode(errors="ignore") for c in base_response.message[0]]).strip()

            return Response(**base_response.__dict__, value=status)
        else: # OBD Commands
            value = None
            parsed_data = list()
            for raw_line in base_response.message[:-1]: # Skip the last line (prompt character)
                line = bytes_to_string(raw_line)
                line = line.replace(' ', '')
                
                if not is_hexadecimal(line):
                    continue # code error handling

                components = split_by_bytes(line)

                if len(components) <= 5: # Skip header-less lines
                    continue

                header = components[0] + components[1]
                bytes_offset = 2 # Mode and PID offset
                length = int(components[2], 16) - bytes_offset

                data = components[-length:]

                parsed_data.append(data)

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