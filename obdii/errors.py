from __future__ import annotations

from re import compile, Pattern
from typing import Set, Type, Optional


class ResponseBaseError(Exception):
    _registry: Set[Type[ResponseBaseError]] = set()

    pattern: Optional[bytes] = None
    regex_pattern: Optional[Pattern] = None

    def __init__(self, response: bytes) -> None:
        self.response = response
        self.message = f"{self.__class__.__name__}: {self.__class__.__doc__} - Got: {str(self.response)}"

        super().__init__(self.message)

    def __init_subclass__(cls, abstract: bool = False, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if abstract:
            return

        if not cls.pattern and not cls.regex_pattern:
            raise TypeError(
                f"{cls.__name__} must define either 'pattern' or 'regex_pattern'"
            )
        ResponseBaseError._registry.add(cls)

    @classmethod
    def detect(cls, response: bytes) -> Optional[ResponseBaseError]:
        """Detect an error in a response and return the corresponding error instance."""
        for err in cls._registry:
            if not issubclass(err, cls):
                continue

            if err.pattern and err.pattern in response:
                return err(response)

            if err.regex_pattern and err.regex_pattern.search(response):
                return err(response)

        return None


# Errors


class ResponseError(ResponseBaseError, abstract=True):
    """Base class for all response errors."""


class InvalidCommandError(ResponseError):
    """The command received on the RS232 input was not recognized or misunderstood."""

    pattern = b'?'


class BufferFullError(ResponseError):
    """The ELM327's 256-byte buffer is full."""

    pattern = b"BUFFER FULL"


class BusBusyError(ResponseError):
    """The ELM327 detected excessive bus activity and was unable to respond."""

    pattern = b"BUS BUSY"


class BusError(ResponseError):
    """A generic error has occurred on the bus."""

    pattern = b"BUS ERROR"


class CanError(ResponseError):
    """The CAN system had difficulty initializing, sending, or receiving."""

    pattern = b"CAN ERROR"


class InvalidDataError(ResponseError):
    """There was a response from the vehicle, but the information was incorrect or could not be recovered."""

    regex_pattern = compile(rb"(?<!<)DATA ERROR")


class InvalidLineError(ResponseError):
    """There was an error in the line that this points to."""

    pattern = b"<DATA ERROR"


class DeviceInternalError(ResponseError):
    """Internal errors reported as ERR with a two digit code following."""

    regex_pattern = compile(rb"ERR\d{2}")


class SignalFeedbackError(ResponseError):
    """Output energized, but input signal not detected. Possible wiring issue. Verify connections."""

    pattern = b"FB ERROR"


class MissingDataError(ResponseError):
    """Vehicle did not respond within timeout."""

    pattern = b"NO DATA"


class CanDataError(ResponseError):
    """Received CAN data contains errors. Verify protocol and baud rate settings."""

    pattern = b"<RX ERROR"


class StoppedError(ResponseError):
    """Operation interrupted by RS232 character or low RTS signal."""

    pattern = b"STOPPED"


class ProtocolConnectionError(ResponseError):
    """No supported protocol detected. Verify vehicle ignition status, compatibility, and connections."""

    pattern = b"UNABLE TO CONNECT"


# Warnings


class ResponseWarning(ResponseBaseError, abstract=True):
    """Base class for all response warnings."""


class InactivityWarning(ResponseWarning):
    """No RS232 activity has been detected for a specified duration (4 or 19 minutes)."""

    pattern = b"ACT ALERT"


class LowPowerWarning(ResponseWarning):
    """The ELM327 is entering Low Power mode in 2 seconds. No interruption possible."""

    pattern = b"LP ALERT"


class LowVoltageResetWarning(ResponseWarning):
    """Indicates low 5V supply voltage, triggering a reset."""

    pattern = b"LV RESET"
