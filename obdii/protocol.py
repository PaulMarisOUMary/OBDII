from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Type, Union


from .basetypes import BaseResponse, Command, Context, Protocol, Response


class BaseProtocol(ABC):
    _registry: Dict[Protocol, Type["BaseProtocol"]] = {}
    _protocol_attributes: Dict[Protocol, Dict] = {}

    extra_init_sequence: List[Union[Command, Callable]]

    def __init__(self) -> None: ...

    @abstractmethod
    def parse_response(self, base_response: BaseResponse, context: Context) -> Response: ...

    @classmethod
    def register(cls, protocols: Dict[Protocol, Dict[str, Any]]) -> None:
        """Register a subclass with its supported protocols."""
        for protocol, attr in protocols.items():
            cls._registry[protocol] = cls
            cls._protocol_attributes[protocol] = attr
    
    @classmethod
    def get_handler(cls, protocol: Protocol) -> "BaseProtocol":
        """Retrieve the appropriate protocol class or fallback to ProtocolUnknown."""
        return cls._registry.get(protocol, ProtocolUnknown)()

    @classmethod
    def get_protocol_attributes(cls, protocol: Protocol) -> Dict[str, Any]:
        return cls._protocol_attributes.get(protocol, {})


class ProtocolUnknown(BaseProtocol): 
    """Fallback protocol class for unknown or unsupported protocols.

    In such cases, basic serial communication might still be possible,
    but full message parsing could be limited.
    """
    def parse_response(self, base_response: BaseResponse, context: Context) -> Response:
        raise NotImplementedError