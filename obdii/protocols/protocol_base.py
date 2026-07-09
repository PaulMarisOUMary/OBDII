from __future__ import annotations

from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import Any, Dict, Mapping, Optional, Type

from ..response import Response, ResponseBase
from ..protocol import Protocol


_EMPTY_ATTRIBUTES: Mapping[str, Any] = MappingProxyType({})


class ProtocolBase(ABC):
    _registry: Dict[Protocol, Type[ProtocolBase]] = {}
    _instances: Dict[Protocol, ProtocolBase] = {}
    _protocol_attributes: Dict[Protocol, Mapping[str, Any]] = {}

    def __init_subclass__(
        cls, protocols: Optional[Dict[Protocol, Dict[str, Any]]] = None, **kwargs
    ) -> None:
        super().__init_subclass__(**kwargs)

        if protocols is not None:
            cls.register(protocols)

    @classmethod
    def register(cls, protocols: Dict[Protocol, Dict[str, Any]]) -> None:
        for protocol, attr in protocols.items():
            if protocol in cls._registry and cls._registry[protocol] is not cls:
                raise ValueError(
                    f"{protocol!r} already registered by {cls._registry[protocol].__name__}"
                )

            cls._registry[protocol] = cls
            cls._protocol_attributes[protocol] = MappingProxyType(dict(attr))
        cls._instances.clear()

    @classmethod
    def get_handler(cls, protocol: Protocol) -> ProtocolBase:
        if protocol not in cls._instances:
            handler_cls = cls._registry.get(protocol, ProtocolUnknown)
            cls._instances[protocol] = handler_cls()
        return cls._instances[protocol]

    @classmethod
    def get_protocol_attributes(cls, protocol: Protocol) -> Mapping[str, Any]:
        return cls._protocol_attributes.get(protocol, _EMPTY_ATTRIBUTES)

    @abstractmethod
    def parse_response(self, response_base: ResponseBase) -> Response: ...


class ProtocolUnknown(ProtocolBase):
    """Fallback protocol class for unknown or unsupported protocols."""

    def parse_response(self, response_base: ResponseBase) -> Response:
        raise NotImplementedError
