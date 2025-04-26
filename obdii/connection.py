from logging import Formatter, Handler, getLogger, INFO
from re import IGNORECASE, search as research
from types import TracebackType
from typing import Callable, List, Optional, Union

from serial import Serial, SerialException # type: ignore

from .basetypes import MISSING
from .command import Command
from .modes import ModeAT
from .protocol import Protocol
from .protocols.protocol_base import BaseProtocol
from .response import BaseResponse, Context, Response
from .utils import bytes_to_string, debug_baseresponse, filter_bytes, setup_logging


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
                    early_return: bool = False,
                    *,
                    log_handler: Handler = MISSING,
                    log_formatter: Formatter = MISSING,
                    log_level: int = INFO,
                    log_root: bool = False,
                ) -> None:
        """
        Initialize connection settings and optionally auto-connect.

        Parameters
        ----------
        port: :class:`str`
            The serial port (e.g., "COM5", "/dev/ttyUSB0", "/dev/rfcomm0").
        baudrate: :class:`int`
            Baud rate for serial communication (e.g., 38400, 115200).
        protocol: :class:`Protocol`
            The protocol to use for communication.
        timeout: :class:`float`
            Timeout in seconds for reading operations.
        write_timeout: :class:`float`
            Timeout in seconds for writing operations.
        auto_connect: :class:`bool`
            If True, connect to the adapter immediately.
        smart_query: :class:`bool`
            If True, send repeat command when the same command is issued again.
        early_return: :class:`bool`
            If set to true, the ELM327 will return immediately after sending the specified number of responses specified in the command (n_bytes). Works only with ELM327 v1.3 and later.
        
        log_handler: :class:`logging.Handler`
            Custom log handler for the logger.
        log_formatter: :class:`logging.Formatter`
            Formatter to use with the given log handler.
        log_level: :class:`int`
            Logging level for the logger.
        log_root: :class:`bool`
            Whether to set up the root logger.
        """
        self.port = port
        self.baudrate = baudrate
        self.protocol = protocol
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.smart_query = smart_query
        self.early_return = early_return

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
        self.init_completed = False

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
        """
        Establish the serial connection and run initialization sequence.

        Parameters
        ----------
        **kwargs: :class:`dict`
            Overrides for connection attributes like `port`, `baudrate`,
            `timeout`, or `write_timeout`. Additional parameters are passed
            directly to the :class:`serial.Serial` constructor.
        """
        overridable_attributes = ["port", "baudrate", "timeout", "write_timeout"]
        for key in set(kwargs.keys()):
            if key in overridable_attributes:
                setattr(self, key, kwargs.pop(key))
                _log.debug(f"Overriding connection attribute '{key}' with '{getattr(self, key)}' from kwargs.")

        _log.info(f"Attempting to connect to {self.port} at {self.baudrate} baud.")
        try:
            self.serial_conn = Serial(
                port = self.port, 
                baudrate = self.baudrate, 
                timeout = self.timeout, 
                write_timeout = self.write_timeout,
                **kwargs
            )
            self._initialize_connection()
            self.init_completed = True
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

    def is_connected(self) -> bool:
        """
        Check if the serial connection is open.

        Returns
        -------
        :class:`bool`
            True if the connection is active.
        """
        return self.serial_conn is not None and self.serial_conn.is_open


    def _auto_protocol(self, protocol: Protocol = MISSING) -> None:
        """Sets the protocol for communication."""
        protocol = protocol or self.protocol
        unwanted_protocols = [Protocol.AUTO, Protocol.UNKNOWN]

        protocol_number = self._set_protocol_to(protocol)

        if Protocol(protocol_number) in unwanted_protocols:
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
        if protocol not in unwanted_protocols and protocol != self.protocol:
            _log.warning(f"Requested protocol {protocol.name} cannot be used.")
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

        self._clear_buffer()
        self.serial_conn.write(query)
        self.serial_conn.flush()
    
    def _read_bytes(self, max_size=4096) -> bytes:
        if not self.serial_conn or not self.serial_conn.is_open:
            _log.error("Attempted to read without an active connection.")
            raise ConnectionError("Attempted to read without an active connection.")
        
        return self.serial_conn.read_until(expected=b'>', size=max_size)


    def query(self, command: Command) -> Response:
        """
        Send a command and wait for the response.

        Parameters
        ----------
        command: :class:`Command`
            Command to send.

        Returns
        -------
        :class:`Response`
            Parsed response from the adapter.
        """      
        if self.smart_query and self.last_command and command == self.last_command:
            query = ModeAT.REPEAT.build()
        else:
            query = command.build(self.early_return)

        context = Context(command, self.protocol)

        self._send_query(query)
        self.last_command = command

        return self.wait_for_response(context)

    def wait_for_response(self, context: Context) -> Response:
        """
        Wait for and parse a response from the adapter.

        Parameters
        ----------
        context: :class:`Context`
            Context to use for parsing.

        Returns
        -------
        :class:`Response`
            Parsed response or raw fallback response.
        """
        raw = self._read_bytes()

        messages = [
            line
            for line in raw.splitlines()
            if line
        ]

        base_response = BaseResponse(context, raw, messages)

        _log.debug(f"<<< Read:\n{debug_baseresponse(base_response)}")

        try:
            return self.protocol_handler.parse_response(base_response)
        except NotImplementedError:
            if self.init_completed:
                _log.warning(f"Unsupported Protocol used: {self.protocol.name}")
            return Response(**vars(base_response))
    

    def _clear_buffer(self) -> None:
        """Clears any buffered input from the adapter."""
        if self.serial_conn:
            self.serial_conn.reset_input_buffer()

    def close(self) -> None:
        """Close the serial connection if not already done."""
        if self.serial_conn:
            self.serial_conn.close()
        self.serial_conn = None
        _log.info("Connection closed.")
    

    def __enter__(self):
        """
        Support usage as a context manager.

        Returns
        -------
        :class:`Connection`
            The connection instance itself.
        """
        return self

    def __exit__(self, exc_type: Optional[BaseException], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        """
        Close the connection when exiting the context.
        """
        self.close()