from dataclasses import dataclass, field
from time import time
from typing import Generic, Optional, List, Dict

from .basetypes import OneOrMany, Real, T
from .command import Command
from .protocol import Protocol


@dataclass
class Context(Generic[T]):
    command: Command[T]
    protocol: Protocol
    timestamp: float = field(default_factory=time)


@dataclass
class ResponseBase(Generic[T]):
    context: Context[T]
    raw: bytes
    timestamp: float = field(default_factory=time)


@dataclass
class Response(ResponseBase, Generic[T]):
    messages: Optional[Dict[bytes, List[int]]] = None
    unparsed: Optional[List[int]] = None

    value: Optional[T] = None

    @property
    def min_values(self) -> Optional[OneOrMany[Real]]:
        return self.context.command.min_values

    @property
    def max_values(self) -> Optional[OneOrMany[Real]]:
        return self.context.command.max_values

    @property
    def units(self) -> Optional[OneOrMany[str]]:
        return self.context.command.units
