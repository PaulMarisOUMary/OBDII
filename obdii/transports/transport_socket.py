from socket import AF_INET, SOCK_STREAM, socket
from typing import Any, Dict, Optional, Union

from ..basetypes import MISSING
from .transport_base import TransportBase


class TransportSocket(TransportBase):
    def __init__(
        self,
        address: str = MISSING,
        port: Union[str, int] = MISSING,
        timeout: float = 5.0,
        **kwargs,
    ) -> None:
        self.config: Dict[str, Any] = {
            "address": address,
            "port": port,
            "timeout": timeout,
            **kwargs,
        }

        self.socket_conn: Optional[socket] = None

        if address is MISSING or port is MISSING:
            raise ValueError(
                "Both address and port must be specified for TransportSocket."
            )

    def __repr__(self) -> str:
        return (
            f"<TransportSocket {self.config.get('address')}:{self.config.get('port')}>"
        )

    def is_connected(self) -> bool:
        if self.socket_conn is None:
            return False
        try:
            self.socket_conn.getpeername()
            return True
        except OSError:
            return False

    def connect(self, **kwargs) -> None:
        self.config.update(kwargs)

        timeout = self.config.get("timeout")
        address = self.config.get("address")
        port = self.config.get("port")

        self.socket_conn = socket(AF_INET, SOCK_STREAM)
        self.socket_conn.settimeout(timeout)
        self.socket_conn.connect((address, port))

    def close(self) -> None:
        if self.socket_conn:
            self.socket_conn.close()
        self.socket_conn = None

    def write_bytes(self, query: bytes) -> None:
        if not self.socket_conn:
            raise RuntimeError("Socket is not connected.")
        self.socket_conn.sendall(query)

    def read_bytes(self, expected_seq: bytes = b'>', size: int = MISSING) -> bytes:
        if not self.socket_conn:
            raise RuntimeError("Socket is not connected.")

        lenterm = len(expected_seq)
        buffer = bytearray()
        while True:
            chunk = self.socket_conn.recv(1)
            if not chunk:
                raise RuntimeError("Socket connection closed.")

            buffer += chunk

            if buffer[-lenterm:] == expected_seq:
                break

            if size is not MISSING and len(buffer) >= size:
                break

        return bytes(buffer)
