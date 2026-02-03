from typing import Optional, Dict, Any

from serial import Serial

from .transport_base import TransportBase

from ..basetypes import MISSING


class TransportSerial(TransportBase):
    def __init__(
        self,
        port: str = MISSING,
        baudrate: int = 38400,
        timeout: float = 5.0,
        write_timeout: float = 3.0,
        **kwargs,
    ) -> None:
        self.config: Dict[str, Any] = {
            "port": port,
            "baudrate": baudrate,
            "timeout": timeout,
            "write_timeout": write_timeout,
            **kwargs,
        }

        self.serial_conn: Optional[Serial] = None

        if port is MISSING:
            raise ValueError("Port must be specified for TransportSerial.")

    def __repr__(self) -> str:
        return f"<TransportSerial {self.config.get('port')} at {self.config.get('baudrate')} baud>"

    def is_connected(self) -> bool:
        return self.serial_conn is not None and self.serial_conn.is_open

    def connect(self, **kwargs) -> None:
        self.config.update(kwargs)

        self.serial_conn = Serial(**self.config)

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
            raise IOError(
                f"Failed to write all bytes to serial port: expected {len(query)}, wrote {written}."
            )

        self.serial_conn.flush()

    def read_bytes(self, expected_seq: bytes = b'>', size: int = MISSING) -> bytes:
        if not self.serial_conn or not self.serial_conn.is_open:
            raise RuntimeError("Serial port is not connected.")
        return self.serial_conn.read_until(
            expected_seq, size if size is not MISSING else None
        )
