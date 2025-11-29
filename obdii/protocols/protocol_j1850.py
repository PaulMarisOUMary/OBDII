from ..protocol import Protocol
from ..response import ResponseBase, Response

from .protocol_base import ProtocolBase


J1850_PROTOCOLS = {
    Protocol.SAE_J1850_PWM: {},
    Protocol.SAE_J1850_VPW: {},
}


class ProtocolJ1850(ProtocolBase, protocols=J1850_PROTOCOLS):
    """Supported Protocols:
    - [0x01] SAE J1850 PWM (41.6 Kbaud)
    - [0x02] SAE J1850 VPW (10.4 Kbaud)
    """

    def parse_response(self, response_base: ResponseBase) -> Response:
        raise NotImplementedError
