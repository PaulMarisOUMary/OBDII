from logging import Formatter, Handler, debug, getLogger
from re import IGNORECASE, search as research
from serial import Serial, SerialException, SerialTimeoutException # type: ignore
from typing import Callable, List, Optional, Union

from .utils import bytes_to_string, debug_baseresponse, filter_bts, setup_logging

from .basetypes import BaseResponse, Command, Protocol, Response
from .modes import ModeAT
from .protocol import BaseProtocol

_log = getLogger(__name__)


class Connection():
    def __init__(self, 
                    port: str,
                    baudrate: int = 38400,
                    protocol: Protocol = Protocol.AUTO,
                    auto_connect: bool = True,
                    smart_query: bool = True,
                    *,
                    log_handler: Optional[Handler] = None,
                    log_formatter: Optional[Formatter] = None,
                    log_level: Optional[int] = None,
                    log_root: bool = False,
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
            self._auto_protocol,
        ]

        self.protocol_preferences = [
            Protocol.ISO_15765_4_CAN,       # 0x06
            Protocol.ISO_15765_4_CAN_B,     # 0x07
            Protocol.ISO_15765_4_CAN_C,     # 0x08
            Protocol.ISO_15765_4_CAN_D,     # 0x09
            Protocol.SAE_J1850_PWM,         # 0x01
            Protocol.SAE_J1850_VPW,         # 0x02
            Protocol.ISO_9141_2,            # 0x03
            Protocol.ISO_14230_4_KWP,       # 0x04
            Protocol.ISO_14230_4_KWP_FAST,  # 0x05 
            Protocol.SAE_J1939_CAN,         # 0x0A
            Protocol.USER1_CAN,             # 0x0B
            Protocol.USER2_CAN,             # 0x0C
        ]

        if log_handler or log_formatter or log_level:
            setup_logging(
                log_handler,
                log_formatter,
                log_level,
                log_root
            )

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

    def _auto_protocol(self, protocol: Optional[Protocol] = None) -> None:
        """Sets the protocol for communication."""
        protocol = protocol or self.protocol

        protocol_number = self._set_protocol_to(protocol)

        if protocol_number in [0, -1]:
            supported_protocols = self._get_supported_protocols()

            if supported_protocols:
                priority_dict = {protocol: idx for idx, protocol in enumerate(self.protocol_preferences)}
                supported_protocols.sort(key=lambda p: priority_dict.get(p, len(self.protocol_preferences)))

                protocol_number = self._set_protocol_to(supported_protocols[0])
            else:
                protocol_number = -1

        self.protocol = Protocol(protocol_number)
        self.protocol_handler = BaseProtocol.get_handler(self.protocol)

    def _set_protocol_to(self, protocol: Protocol) -> int:
        """Attempts to set the protocol to the specified value, return the protocol number if successful."""
        self.query(ModeAT.SET_PROTOCOL(protocol.value))
        response = self.query(ModeAT.DESC_PROTOCOL_N)

        line = bytes_to_string(response.raw_response, [b'\r', b'>'])
        protocol_number = self._parse_protocol_number(line)

        return protocol_number

    def _get_supported_protocols(self) -> List[Protocol]:
        """Attempts to find supported protocol(s)."""
        supported_protocols = []

        for protocol in Protocol:
            if protocol in [Protocol.UNKNOWN, Protocol.AUTO]:
                continue

            protocol_number = self._set_protocol_to(protocol)
            if protocol_number == protocol.value:
                supported_protocols.append(protocol)

        return supported_protocols if supported_protocols else [Protocol.UNKNOWN]

    def _parse_protocol_number(self, line: str) -> int:
        """Extracts and returns the protocol number from the response line."""
        match = research(r"(\d)$", line, IGNORECASE)
        if match:
            return int(match.group(1), 16)
        return -1

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

        _log.debug(f">>> Send: {str(query)}")

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

        _log.debug(f"<<< Read:\n{debug_baseresponse(base_response)}")

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