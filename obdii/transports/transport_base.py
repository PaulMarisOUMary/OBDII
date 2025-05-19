from abc import ABC, abstractmethod


class TransportBase(ABC):
    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def write_bytes(self, query: bytes) -> None: ...

    @abstractmethod
    def read_bytes(self) -> bytes: ...

    @abstractmethod
    def is_connected(self) -> bool: ...

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"<{self.__class__.__name__}({attrs})>"