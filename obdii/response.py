from dataclasses import dataclass, field
from time import time
from typing import Any, List, Optional

from .basetypes import BytesRows, OneOrMany, Real
from .command import Command
from .protocol import Protocol


@dataclass
class Context():
    command: Command
    protocol: Protocol
    timestamp: float = field(default_factory=time)


@dataclass
class BaseResponse():
    context: Context
    raw: bytes
    messages: List[bytes]
    timestamp: float = field(default_factory=time)


@dataclass
class Response(BaseResponse):
    parsed_data: Optional[BytesRows] = None

    value: Optional[Any] = None

    @property
    def min_values(self) -> Optional[OneOrMany[Real]]:
        return self.context.command.min_values
    
    @property
    def max_values(self) -> Optional[OneOrMany[Real]]:
        return self.context.command.max_values
    
    @property
    def units(self) -> Optional[OneOrMany[str]]:
        return self.context.command.units
