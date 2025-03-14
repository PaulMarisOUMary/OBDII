from typing import Callable, List, Optional, Union
from serial import Serial, SerialException, SerialTimeoutException # type: ignore

from .basetypes import BaseResponse, Command, Protocol, Response
from .modes import ModeAT
from .protocol import BaseProtocol


class Connection():
    def __init__(self, 
                    port: str,
                    baudrate: int = 38400,
                    protocol: Protocol = Protocol.AUTO,
                    auto_connect: bool = True,
                    smart_query: bool = True,
                ) -> None:
        """Initialize connection settings and auto-connect by default.

        Attributes
        -----------
        port: :class:`str`
            The serial port (e.g., "COM5", "/dev/ttyUSB0", "/dev/rfcomm0").
        baudrate: :class:`int`
            The baud rate for communication (e.g., 38400, 115200).
        protocol: :class:`Protocol`
            The protocol to use for communication (default: Protocol.AUTO).
        auto_connect: Optional[:class:`bool`]
            If set to true, method connect will be called.
        smart_query: Optional[:class:`bool`]
            If set to true, and if the same command is sent twice, the second time it will be sent as a repeat command.
        """
        self.port = port
        self.baudrate = baudrate
        self.protocol = protocol
        self.smart_query = smart_query

        self.serial_conn: Optional[Serial] = None
        self.protocol_handler = BaseProtocol.get_handler(Protocol.UNKNOWN)
        self.last_command: Optional[Command] = None

        self.timeout = 5.0
        self.write_timeout = 3.0

        self.init_sequence: List[Union[Command, Callable]] = [
            ModeAT.RESET,
            ModeAT.ECHO_OFF,
            ModeAT.LINEFEED_OFF,
            ModeAT.HEADERS_ON,
            ModeAT.SPACES_ON,
            self._set_protocol,
        ]

        if auto_connect:
            self.connect()

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
        """Initializes the connection using the init sequence."""
        for command in self.init_sequence:
            if isinstance(command, Command):
                self.query(command)
            elif callable(command):
                command()
            else:
                raise TypeError(f"Invalid command type: {type(command)}")
    
    def _set_protocol(self, protocol: Optional[Protocol] = None) -> None:
        """Sets the protocol for communication."""
        protocol = protocol or self.protocol

        self.query(ModeAT.SET_PROTOCOL(protocol.value))
        protocol_response = self.query(ModeAT.DESC_PROTOCOL_N)

        try:
            self.protocol = Protocol(int(protocol_response.raw_response[1], 16))
        except ValueError:
            self.protocol = Protocol.UNKNOWN

        self.protocol_handler = BaseProtocol.get_handler(self.protocol)

    def _send_query(self, query: bytes) -> None:
        """Sends a query to the ELM327."""
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("Attempted to send a query without an active connection.")

        self.clear_buffer()
        self.serial_conn.write(query)
        self.serial_conn.flush()
    
    def _read_byte(self) -> bytes:
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("Attempted to read without an active connection.")
        
        return self.serial_conn.read(1)

    def query(self, command: Command) -> Response:
        """Sends a command and waits for a response."""        
        if self.smart_query and self.last_command and command == self.last_command:
            query = ModeAT.REPEAT.build()
        else:
            query = command.build()

        self._send_query(query)
        self.last_command = command

        return self.wait_for_response(command)

    def wait_for_response(self, command: Command) -> Response:
        """Reads data dynamically until the OBDII prompt (>) or timeout."""
        raw_response: List[bytes] = []

        message: List[List[bytes]] = []
        current_line: List[bytes] = []
        while True:
            chunk = self._read_byte()
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


        try:
            return self.protocol_handler.parse_response(base_response, command)
        except NotImplementedError:
            return Response(**base_response.__dict__)
    
    def clear_buffer(self) -> None:
        """Clears any buffered input from the adapter."""
        if self.serial_conn:
            self.serial_conn.reset_input_buffer()

    def close(self) -> None:
        """Close the serial connection if not already done."""
        if self.serial_conn:
            self.serial_conn.close()