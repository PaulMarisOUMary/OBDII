from logging import Formatter, Handler, getLogger, INFO
from re import IGNORECASE, search as research
from types import TracebackType
from serial import Serial, SerialException # type: ignore
from typing import Callable, List, Optional, Union

from .utils import bytes_to_string, debug_baseresponse, filter_bytes, setup_logging

from .basetypes import BaseResponse, Command, Context, Protocol, Response
from .modes import ModeAT
from .protocol import BaseProtocol

_log = getLogger(__name__)


class Connection():
    def __init__(self, 
                    port: str,
                    baudrate: int = 38400,
                    protocol: Protocol = Protocol.AUTO,
                    timeout: float = 5.0,
                    write_timeout: float = 3.0,
                    auto_connect: bool = True,
                    smart_query: bool = False,
                    *,
                    log_handler: Optional[Handler] = None,
                    log_formatter: Optional[Formatter] = None,
                    log_level: Optional[int] = INFO,
                    log_root: bool = False,
                ) -> None:
        """Initialize connection settings and auto-connect by default.

        Parameters
        -----------
        port: :class:`str`
            The serial port (e.g., "COM5", "/dev/ttyUSB0", "/dev/rfcomm0").
        baudrate: :class:`int`
            The baud rate for communication (e.g., 38400, 115200).
        protocol: :class:`Protocol`
            The protocol to use for communication (default: Protocol.AUTO).
        timeout: :class:`float`
            The maximum time (in seconds) to wait for a response from the device before raising a timeout error (default: 5.0).
        write_timeout: :class:`float`
            The time (in seconds) to wait for data to be written to the device before raising a timeout error (default: 3.0).
        auto_connect: Optional[:class:`bool`]
            If set to true, method connect will be called.
        smart_query: Optional[:class:`bool`]
            If set to true, and if the same command is sent twice, the second time it will be sent as a repeat command.

        *:
            Keyword-only arguments (non-positional).


        log_handler: Optional[:class:`logging.Handler`]
            The log handler to use for the library's logger.
        log_formatter: :class:`logging.Formatter`
            The formatter to use with the given log handler.
        log_level: :class:`int`
            The default log level for the library's logger.
        root_logger: :class:`bool`
            Whether to set up the root logger rather than the library logger.
        """
        self.port = port
        self.baudrate = baudrate
        self.protocol = protocol
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.smart_query = smart_query

        self.serial_conn: Optional[Serial] = None
        self.protocol_handler = BaseProtocol.get_handler(Protocol.UNKNOWN)
        self.supported_protocols: List[Protocol] = []
        self.last_command: Optional[Command] = None

        self.init_sequence: List[Union[Command, Callable[[], None]]] = [
            ModeAT.RESET,
            ModeAT.ECHO_OFF,
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
            _log.info(f"Attempting to connect to {self.port} at {self.baudrate} baud.")
            self.serial_conn = Serial(
                port=self.port, 
                baudrate=self.baudrate, 
                timeout=self.timeout, 
                write_timeout=self.write_timeout,
                **kwargs
            )
            self._initialize_connection()
            _log.info(f"Successfully connected to {self.port}.")
        except SerialException as e:
            self.serial_conn = None
            _log.error(f"Failed to connect to {self.port}: {e}")
            raise ConnectionError(f"Failed to connect: {e}")

    def _initialize_connection(self) -> None:
        """Initializes the connection using the init sequence."""
        for command in self.init_sequence:
            if isinstance(command, Command):
                self.query(command)
            elif callable(command):
                command()
            else:
                _log.error(f"Invalid type in init_sequence: {type(command)}")
                raise TypeError(f"Invalid command type: {type(command)}")


    def _auto_protocol(self, protocol: Optional[Protocol] = None) -> None:
        """Sets the protocol for communication."""
        protocol = protocol or self.protocol

        protocol_number = self._set_protocol_to(protocol)

        if protocol_number in [0, -1]:
            self.supported_protocols = self._get_supported_protocols()
            supported_protocols = self.supported_protocols

            if supported_protocols:
                priority_dict = {protocol: idx for idx, protocol in enumerate(self.protocol_preferences)}
                supported_protocols.sort(key=lambda p: priority_dict.get(p, len(self.protocol_preferences)))

                protocol_number = self._set_protocol_to(supported_protocols[0])
            else:
                protocol_number = -1

        self.protocol = Protocol(protocol_number)
        self.protocol_handler = BaseProtocol.get_handler(self.protocol)
        _log.info(f"Protocol set to {self.protocol.name}.")

    def _set_protocol_to(self, protocol: Protocol) -> int:
        """Attempts to set the protocol to the specified value, return the protocol number if successful."""
        self.query(ModeAT.SET_PROTOCOL(protocol.value))
        response = self.query(ModeAT.DESC_PROTOCOL_N)

        line = bytes_to_string(filter_bytes(response.raw, b'\r', b'>'))
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
        
        if not supported_protocols:
            _log.warning("No supported protocols detected.")
            supported_protocols = [Protocol.UNKNOWN]

        return supported_protocols

    def _parse_protocol_number(self, line: str) -> int:
        """Extracts and returns the protocol number from the response line."""
        match = research(r"([0-9A-F])$", line, IGNORECASE)
        if match:
            return int(match.group(1), 16)
        return -1


    def _send_query(self, query: bytes) -> None:
        """Sends a query to the ELM327."""
        if not self.serial_conn or not self.serial_conn.is_open:
            _log.error("Attempted to send a query without an active connection.")
            raise ConnectionError("Attempted to send a query without an active connection.")

        _log.debug(f">>> Send: {str(query)}")

        self.clear_buffer()
        self.serial_conn.write(query)
        self.serial_conn.flush()
    
    def _read_bytes(self, max_size=4096) -> bytes:
        if not self.serial_conn or not self.serial_conn.is_open:
            _log.error("Attempted to read without an active connection.")
            raise ConnectionError("Attempted to read without an active connection.")
        
        return self.serial_conn.read_until(expected=b'>', size=max_size)


    def query(self, command: Command) -> Response:
        """Sends a command and waits for a response."""        
        if self.smart_query and self.last_command and command == self.last_command:
            query = ModeAT.REPEAT.build()
        else:
            query = command.build()

        context = Context(command, self.protocol)

        self._send_query(query)
        self.last_command = command

        return self.wait_for_response(context)

    def wait_for_response(self, context: Context) -> Response:
        """Reads data dynamically until the OBDII prompt (>) or timeout."""
        raw = self._read_bytes()

        messages = [
            line
            for line in raw.splitlines()
            if line
        ]

        base_response = BaseResponse(context, raw, messages)

        _log.debug(f"<<< Read:\n{debug_baseresponse(base_response)}")

        try:
            return self.protocol_handler.parse_response(base_response, context)
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
            _log.debug("Connection closed.")
    

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Optional[BaseException], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        self.close()