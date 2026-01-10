from __future__ import annotations

from enum import Enum
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)


T = TypeVar('T')


E = TypeVar('E', bound="BaseEnum")


class BaseEnum(Enum):
    @overload
    @classmethod
    def get_from(cls: Type[E], other: Any, /) -> Union[E, None]: ...

    @overload
    @classmethod
    def get_from(cls: Type[E], other: Any, /, default: T) -> Union[E, T]: ...

    @classmethod
    def get_from(
        cls: Type[E], other: Any, /, default: Union[T, None] = None
    ) -> Union[E, T, None]:
        if isinstance(other, cls):
            return other

        elif isinstance(other, str):
            if other in cls:
                return cls(other)
            try:
                normalized = other.lstrip('0') or '0'
                other = int(normalized, 0)
            except ValueError:
                return default

        if isinstance(other, int):
            for item in cls:
                if item.value == other:
                    return item

        return default

    @classmethod
    def has(cls, other: Any) -> bool:
        return cls.get_from(other) is not None


class SingletonMeta(type):
    _instances: Dict[type, object] = {}

    def __call__(cls, *args, **kwargs) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class _MissingSentinel(metaclass=SingletonMeta):
    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, _MissingSentinel)

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> Literal["..."]:
        return "..."


MISSING: Any = _MissingSentinel()

OneOrMany = Union[T, Iterable[T]]

Real = Union[int, float]

BytesRows = List[Tuple[bytes, ...]]
