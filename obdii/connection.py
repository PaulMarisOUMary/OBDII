from typing import Optional
from serial import Serial, SerialException, SerialTimeoutException # type: ignore

from .basetypes import Command
from .modes.modeat import ModeAT


class Connection():
    def __init__(self, 
                    port: str,
                    baudrate: int = 38400,
                    auto_connect: bool = True,
                    **serial_kwargs
                ) -> None:
        """Initialize connection settings and auto-connect by default.

        Attributes
        -----------
        port: :class:`str`
            The serial port (e.g., "COM5", "/dev/ttyUSB0", "/dev/rfcomm0").
        baudrate: :class:`int`
            The baud rate for communication (e.g., 38400, 115200).
        auto_connect: Optional[:class:`bool`]
            If set to true, method connect will be called.
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_conn: Optional[Serial] = None

        self.timeout = 5.0
        self.write_timeout = 3.0

        for key in list(serial_kwargs.keys()):
            if not callable(getattr(self, key, None)):
                setattr(self, key, serial_kwargs.pop(key))

        self.serial_kwargs = serial_kwargs

        if auto_connect:
            self.connect(**serial_kwargs)

    def connect(self, **kwargs) -> None:
        """Establishes a connection and initializes the device."""
        try:
            self.serial_conn = Serial(
                self.port, 
                self.baudrate, 
                timeout=self.timeout, 
                write_timeout=self.write_timeout,
                **kwargs
            )
            self._initialize_connection()
        except SerialException as e:
            self.serial_conn = None
            raise ConnectionError(f"Failed to connect: {e}")
        
    def _initialize_connection(self) -> None:
        """Initializes the device by resetting and disabling echo."""
        if not self.serial_conn:
            raise ConnectionError("Attempted to initialize without an active connection.")

        self.query(ModeAT.RESET)

        echo_response = self.query(ModeAT.ECHO_OFF)
        if "OK" not in echo_response:
            raise ConnectionError(f"Failed to disable echo, received: {echo_response}")

    def query(self, command: Command) -> str:
        """Sends a command and waits for a response."""
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionRefusedError("Connection is not open")

        query = self.build_command(command)
        self.clear_buffer()
        self.serial_conn.write(query)
        self.serial_conn.flush()

        return self.wait_for_prompt()

    def wait_for_prompt(self) -> str:
        """Reads data dynamically until the OBDII prompt (>) or timeout."""
        if not self.serial_conn or not self.serial_conn.is_open:
            return ""

        response = []
        while True:
            chunk = self.serial_conn.read(1).decode(errors="ignore")
            if not chunk: # Timeout
                break
            if chunk in ['\r']:
                continue
            if chunk == ">":
                break
            response.append(chunk)

        full_response = "".join(response).strip()

        if full_response and full_response != ">":
            return full_response
        return ""
    
    def clear_buffer(self) -> None:
        """Clears any buffered input from the adapter."""
        if self.serial_conn:
            self.serial_conn.reset_input_buffer()

    def build_command(self, command: Command) -> bytes:
        """ELM327 is not case-sensitive, ignores spaces and all control characters."""
        mode = command.mode.value
        pid = command.pid
        if isinstance(command.mode.value, int):
            mode = f"{command.mode.value:02X}"
        if isinstance(pid, int):
            pid = f"{command.pid:02X}"
        return f"{mode}{pid}\r".encode()

    def close(self) -> None:
        """Close the serial connection if not already done."""
        if self.serial_conn:
            self.serial_conn.close()