from socket import AF_INET, SOCK_STREAM, error as s_error, socket
from typing import Optional, Union

from .transport_base import TransportBase

from ..basetypes import MISSING
from ..utils.helper import override_class_attributes


class TransportWifi(TransportBase):
    def __init__(self, **kwargs) -> None:
        self.overridable_attributes = {
            "address": MISSING,
            "port": MISSING,
            "timeout": 5.0,
        }

        self.address: str
        self.port: Union[str, int]
        self.timeout: float

        self.socket_conn: Optional[socket] = None

        override_class_attributes(self, self.overridable_attributes, **kwargs)

        if self.address is MISSING or self.port is MISSING:
            raise ValueError("Both address and port must be specified for TransportWifi.")


    def __repr__(self) -> str:
        return f"<TransportWifi {self.address}:{self.port}>"


    def is_connected(self) -> bool:
        if self.socket_conn is None:
            return False
        try:
            self.socket_conn.getpeername()
            return True
        except s_error:
            return False


    def connect(self, **kwargs) -> None:
        override_class_attributes(self, self.overridable_attributes, True, **kwargs)

        self.socket_conn = socket(AF_INET, SOCK_STREAM)
        self.socket_conn.settimeout(self.timeout)
        self.socket_conn.connect((self.address, int(self.port)))

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