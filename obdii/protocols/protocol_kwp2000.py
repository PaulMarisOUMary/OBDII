from ..protocol import Protocol
from ..response import ResponseBase, Response

from .protocol_base import ProtocolBase


KWP2000_PROTOCOLS = {
    Protocol.ISO_9141_2: {},
    Protocol.ISO_14230_4_KWP: {},
    Protocol.ISO_14230_4_KWP_FAST: {},
}


class ProtocolKWP2000(ProtocolBase, protocols=KWP2000_PROTOCOLS):
    """Supported Protocols:
    - [0x03] ISO 9141-2 (5 baud init, 10.4 Kbaud)
    - [0x04] ISO 14230-4 KWP (5 baud init, 10.4 Kbaud)
    - [0x05] ISO 14230-4 KWP (fast init, 10.4 Kbaud)
    """

    def parse_response(self, response_base: ResponseBase) -> Response:
        raise NotImplementedError
