from typing import List, Optional
from serial import Serial, SerialException, SerialTimeoutException # type: ignore

from .basetypes import BaseResponse, Command, Mode
from .modes.modeat import ModeAT


class Connection():
    def __init__(self, 
                    port: str,
                    baudrate: int = 38400,
                    auto_connect: bool = True,
                    smart_query: bool = True,
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
        self.smart_query = smart_query
        self.last_command: Optional[Command] = None

        self.timeout = 5.0
        self.write_timeout = 3.0

        self.init_sequence = [
            ModeAT.RESET,
            ModeAT.ECHO_OFF,
            ModeAT.LINEFEED_OFF,
            ModeAT.HEADERS_ON,
            ModeAT.SPACES_ON,
        ]

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

        for command in self.init_sequence:
            self.query(command)

    def _send_query(self, query: bytes) -> None:
        """Sends a query to the ELM327."""
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionRefusedError("Connection is not open")

        self.clear_buffer()
        self.serial_conn.write(query)
        self.serial_conn.flush()

    def query(self, command: Command) -> str:
        """Sends a command and waits for a response."""        
        if self.smart_query and self.last_command and command == self.last_command:
            query = self.build_command(ModeAT.REPEAT)
        else:
            query = self.build_command(command)

        self._send_query(query)
        self.last_command = command

        return self.wait_for_response(command)

    def wait_for_response(self, command: Command) -> str:
        """Reads data dynamically until the OBDII prompt (>) or timeout."""
        if not self.serial_conn or not self.serial_conn.is_open:
            return ""

        raw_response: List[bytes] = []

        message: List[List[bytes]] = []
        current_line: List[bytes] = []
        while True:
            chunk = self.serial_conn.read(1)
            if not chunk: # Timeout
                break
            raw_response.append(chunk)
            char = chunk.decode(errors="ignore")

            if char in ['\r', '\n']:
                if current_line:
                    message.append(current_line)
                    current_line = []
                continue
            current_line.append(chunk)
            if char == '>': # Ending prompt character
                break
        if current_line:
            message.append(current_line)

        base_response = BaseResponse(command, raw_response, message)



            return full_response
        return ""
    
    def parse_response(self, raw_response: List[str], command: Optional[Command]) -> str:
        line = ''.join(raw_response).strip()
        if command and command.mode != Mode.AT:
            try:
                data = line.split(' ')

                bytes_offset = 2 # Mode and PID offset
                length = int(data[1], 16) - bytes_offset

                response = data[-length:]
                
                return ''.join(response)
            except IndexError:
                return line
        return line
    
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