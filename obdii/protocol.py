from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Type, Union


from .basetypes import BaseResponse, Command, Protocol, Response


class BaseProtocol(ABC):
    _registry: Dict[Protocol, Type["BaseProtocol"]] = {}

    extra_init_sequence: List[Union[Command, Callable]]

    def __init__(self) -> None: ...

    @abstractmethod
    def parse_response(self, base_response: BaseResponse, command: Command) -> Response: ...

    @classmethod
    def register(cls, *protocols: Protocol) -> None:
        """Register a subclass with its supported protocols."""
        for protocol in protocols:
            cls._registry[protocol] = cls
    
    @classmethod
    def get_handler(cls, protocol: Protocol) -> "BaseProtocol":
        """Retrieve the appropriate protocol class or fallback to ProtocolUnknown."""
        return cls._registry.get(protocol, ProtocolUnknown)()


class ProtocolJ1850(BaseProtocol):
    """Supported Protocols:
    - [0x01] SAE J1850 PWM (41.6 Kbaud)
    - [0x02] SAE J1850 VPW (10.4 Kbaud)
    """
    def parse_response(self, base_response: BaseResponse, command: Command) -> Response:
        raise NotImplementedError

ProtocolJ1850.register(Protocol.SAE_J1850_PWM, Protocol.SAE_J1850_VPW)


class ProtocolKWP2000(BaseProtocol):
    """Supported Protocols:
    - [0x03] ISO 9141-2 (5 baud init, 10.4 Kbaud)
    - [0x04] ISO 14230-4 KWP (5 baud init, 10.4 Kbaud)
    - [0x05] ISO 14230-4 KWP (fast init, 10.4 Kbaud)
    """
    def parse_response(self, base_response: BaseResponse, command: Command) -> Response:
        raise NotImplementedError

ProtocolKWP2000.register(Protocol.ISO_9141_2, Protocol.ISO_14230_4_KWP, Protocol.ISO_14230_4_KWP_FAST)


class ProtocolUnknown(BaseProtocol): 
    """Fallback protocol class for unknown or unsupported protocols.

    In such cases, basic serial communication might still be possible,
    but full message parsing could be limited.
    """
    def parse_response(self, base_response: BaseResponse, command: Command) -> Response:
        raise NotImplementedError