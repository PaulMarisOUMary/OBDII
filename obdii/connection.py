from logging import Formatter, Handler, getLogger, INFO
from re import IGNORECASE, search as research
from types import TracebackType
from typing import Callable, List, Optional, Tuple, Union

from .basetypes import MISSING
from .command import Command
from .modes import ModeAT
from .protocol import Protocol
from .protocols.protocol_base import ProtocolBase
from .response import Context, Response, ResponseBase
from .transports.transport_base import TransportBase
from .transports import TransportPort, TransportWifi
from .utils.bits import bytes_to_string, filter_bytes
from .utils.helper import debug_responsebase, setup_logging


_log = getLogger(__name__)


class Connection():
    def __init__(self, 
                    transport: Union[str, Tuple[str, Union[str, int]], TransportBase],
                    protocol: Protocol = Protocol.AUTO,
                    auto_connect: bool = True,
                    smart_query: bool = False,
                    early_return: bool = False,
                    *,
                    log_handler: Handler = MISSING,
                    log_formatter: Formatter = MISSING,
                    log_level: int = INFO,
                    log_root: bool = False,
                    **kwargs,
                ) -> None:
        """
        Initialize connection settings and optionally auto-connect.

        Parameters
        ----------
        transport: Union[:class:`str`, Tuple[:class:`str`, Union[:class:`str`, :class:`int`]], :class:`obdii.transports.transport_base.TransportBase`]
            Can be represented as a string for serial ports (e.g., "COM5", "/dev/ttyUSB0", "/dev/rfcomm0"),
            or as a tuple for network transports (e.g., ("<hostname>", <port>)),
            or as an instance of a subclass of :class:`obdii.transports.transport_base.TransportBase`.
        protocol: :class:`Protocol`
            The protocol to use for communication.
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
        
        **kwargs: :class:`dict`
            Additional keyword arguments to pass to the transport's connect method. Only used if `auto_connect` is True.
        """
        self.transport = self._resolve_transport(transport, **kwargs)

        self.protocol = protocol
        self.smart_query = smart_query
        self.early_return = early_return

        self.protocol_handler = ProtocolBase.get_handler(Protocol.UNKNOWN)
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
            self.connect(**kwargs)
    

    def _resolve_transport(self, transport: Union[str, Tuple[str, Union[str, int]], TransportBase], **kwargs) -> TransportBase:
        """Resolves a user-supplied transport input into a concrete TransportBase instance."""
        if isinstance(transport, str):
            return TransportPort(port=transport, **kwargs)
        elif isinstance(transport, tuple) \
            and len(transport) == 2 \
            and isinstance(transport[0], str) \
            and isinstance(transport[1], (str, int)):
            return TransportWifi(address=transport[0], port=transport[1], **kwargs)
        elif isinstance(transport, TransportBase):
            return transport
        else:
            raise TypeError(f"Invalid transport type: {type(transport)}.")


    def connect(self, **kwargs) -> None:
        """
        Establishes a connection to the device using the configured transport and runs the initialization sequence.

        Parameters
        ----------
        **kwargs
            Additional parameters forwarded to the transport's `connect()` method.
        """
        _log.info(f"Attempting to connect to {repr(self.transport)}.")
        try:
            self.transport.connect(**kwargs)
            self._initialize_connection()
            self.init_completed = True
            _log.info(f"Successfully connected to {repr(self.transport)}.")
        except Exception as e:
            self.transport.close()
            _log.error(f"Failed to connect to {repr(self.transport)}: {e}")
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
        Checks if the transport connection is open.

        Returns
        -------
        :class:`bool`
            True if the connection is active.
        """
        return self.transport.is_connected()


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
        self.protocol_handler = ProtocolBase.get_handler(self.protocol)
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

        _log.debug(f">>> Send: {str(query)}")

        self.transport.write_bytes(query)
        self.last_command = command

        return self.wait_for_response(context)

    def wait_for_response(self, context: Context) -> Response:
        """
        Wait for a raw response from the transport and parses it using the protocol handler.

        Parameters
        ----------
        context: :class:`Context`
            Context to use for parsing.

        Returns
        -------
        :class:`Response`
            Parsed response or raw fallback response.
        """
        raw = self.transport.read_bytes()

        messages = [
            line
            for line in raw.splitlines()
            if line
        ]

        response_base = ResponseBase(context, raw, messages)

        _log.debug(f"<<< Read:\n{debug_responsebase(response_base)}")

        try:
            return self.protocol_handler.parse_response(response_base)
        except NotImplementedError:
            if self.init_completed:
                _log.warning(f"Unsupported Protocol used: {self.protocol.name}")
            return Response(**vars(response_base))


    def close(self) -> None:
        """
        Closes the transport connection.
        """
        self.transport.close()
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