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


class ProtocolUnknown(BaseProtocol): 
    """Fallback protocol class for unknown or unsupported protocols.

    In such cases, basic serial communication might still be possible,
    but full message parsing could be limited.
    """
    def parse_response(self, base_response: BaseResponse, command: Command) -> Response:
        raise NotImplementedError