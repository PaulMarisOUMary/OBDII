from ..basetypes import BaseResponse, Command, Mode, Protocol, Response
from ..protocol import BaseProtocol


class ProtocolKWP2000(BaseProtocol):
    """Supported Protocols:
    - [0x03] ISO 9141-2 (5 baud init, 10.4 Kbaud)
    - [0x04] ISO 14230-4 KWP (5 baud init, 10.4 Kbaud)
    - [0x05] ISO 14230-4 KWP (fast init, 10.4 Kbaud)
    """
    def parse_response(self, base_response: BaseResponse, command: Command) -> Response:
        raise NotImplementedError


ProtocolKWP2000.register(Protocol.ISO_9141_2, Protocol.ISO_14230_4_KWP, Protocol.ISO_14230_4_KWP_FAST)