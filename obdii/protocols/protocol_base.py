from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, List

from ..protocol import Protocol
from ..response import ResponseBase, Response


class ProtocolBase(ABC):
    _registry: Dict[Protocol, Type[ProtocolBase]] = {}
    _protocol_attributes: Dict[Protocol, Dict] = {}

    def __init__(self) -> None: ...

    def __init_subclass__(
        cls, protocols: Optional[Dict[Protocol, Dict[str, Any]]] = None, **kwargs
    ) -> None:
        super().__init_subclass__(**kwargs)
        if protocols is not None:
            cls.register(protocols)

    @classmethod
    def register(cls, protocols: Dict[Protocol, Dict[str, Any]]) -> None:
        """Register a subclass with its supported protocols."""
        for protocol, attr in protocols.items():
            cls._registry[protocol] = cls
            cls._protocol_attributes[protocol] = attr

    @classmethod
    def get_handler(cls, protocol: Protocol) -> ProtocolBase:
        """Retrieve the appropriate protocol class or fallback to ProtocolUnknown."""
        handler_cls = cls._registry.get(protocol, ProtocolUnknown)
        return handler_cls()

    @classmethod
    def get_protocol_attributes(cls, protocol: Protocol) -> Dict[str, Any]:
        return cls._protocol_attributes.get(protocol, {})

    @staticmethod
    def to_lines(raw: bytes) -> List[bytes]:
        return [
            line for line in raw.splitlines() if line.strip() and line.strip() != b'>'
        ]

    @abstractmethod
    def parse_response(self, response_base: ResponseBase) -> Response: ...


class ProtocolUnknown(ProtocolBase):
    """Fallback protocol class for unknown or unsupported protocols.

    In such cases, basic serial communication might still be possible,
    but full message parsing could be limited.
    """

    def parse_response(self, response_base: ResponseBase) -> Response:
        raise NotImplementedError
