from typing import Any, Dict, Iterable, List, Literal, Tuple, TypeVar, Union


T = TypeVar('T')

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