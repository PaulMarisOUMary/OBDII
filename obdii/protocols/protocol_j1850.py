from ..basetypes import BaseResponse, Context, Protocol, Response
from ..protocol import BaseProtocol


class ProtocolJ1850(BaseProtocol):
    """Supported Protocols:
    - [0x01] SAE J1850 PWM (41.6 Kbaud)
    - [0x02] SAE J1850 VPW (10.4 Kbaud)
    """
    def parse_response(self, base_response: BaseResponse, context: Context) -> Response:
        raise NotImplementedError


ProtocolJ1850.register({
    Protocol.SAE_J1850_PWM: {},
    Protocol.SAE_J1850_VPW: {},
})