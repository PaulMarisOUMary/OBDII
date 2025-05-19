from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from ..protocol import Protocol
from ..response import ResponseBase, Response


class ProtocolBase(ABC):
    _registry: Dict[Protocol, Type[ProtocolBase]] = {}
    _protocol_attributes: Dict[Protocol, Dict] = {}

    def __init__(self) -> None: ...

    @abstractmethod
    def parse_response(self, response_base: ResponseBase) -> Response: ...

    @classmethod
    def register(cls, protocols: Dict[Protocol, Dict[str, Any]]) -> None:
        """Register a subclass with its supported protocols."""
        for protocol, attr in protocols.items():
            cls._registry[protocol] = cls
            cls._protocol_attributes[protocol] = attr

    @classmethod
    def get_handler(cls, protocol: Protocol) -> ProtocolBase:
        """Retrieve the appropriate protocol class or fallback to ProtocolUnknown."""
        return cls._registry.get(protocol, ProtocolUnknown)()

    @classmethod
    def get_protocol_attributes(cls, protocol: Protocol) -> Dict[str, Any]:
        return cls._protocol_attributes.get(protocol, {})


class ProtocolUnknown(ProtocolBase): 
    """Fallback protocol class for unknown or unsupported protocols.

    In such cases, basic serial communication might still be possible,
    but full message parsing could be limited.
    """
    def parse_response(self, response_base: ResponseBase) -> Response:
        raise NotImplementedError