from typing import Optional

from serial import Serial # type: ignore

from .transport_base import TransportBase

from ..basetypes import MISSING
from ..utils.helper import override_class_attributes


class TransportPort(TransportBase):
    def __init__(self, **kwargs) -> None:
        self.overridable_attributes = {
            "port": MISSING,
            "baudrate": 38400,
            "timeout": 5.0,
            "write_timeout": 3.0,
        }

        self.port: str
        self.baudrate: int
        self.timeout: float
        self.write_timeout: float

        self.serial_conn: Optional[Serial] = None

        override_class_attributes(self, self.overridable_attributes, **kwargs)

        if self.port is MISSING:
            raise ValueError("Port must be specified for TransportPort.")


    def __repr__(self) -> str:
        return f"<TransportPort {self.port} at {self.baudrate} baud>"


    def is_connected(self) -> bool:
        return self.serial_conn is not None and self.serial_conn.is_open


    def connect(self, **kwargs) -> None:
        override_class_attributes(self, self.overridable_attributes, True, **kwargs)

        self.serial_conn = Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout,
            write_timeout=self.write_timeout,
            **kwargs,
        )

    def close(self) -> None:
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        self.serial_conn = None


    def write_bytes(self, query: bytes) -> None:
        if not self.serial_conn or not self.serial_conn.is_open:
            raise RuntimeError("Serial port is not connected.")
        self.serial_conn.reset_input_buffer()

        written = self.serial_conn.write(query)
        if written != len(query):
            raise IOError(f"Failed to write all bytes to serial port: expected {len(query)}, wrote {written}.")

        self.serial_conn.flush()

    def read_bytes(self, expected_seq: bytes = b'>', size: int = 4096) -> bytes:
        if not self.serial_conn or not self.serial_conn.is_open:
            raise RuntimeError("Serial port is not connected.")
        return self.serial_conn.read_until(expected_seq, size)