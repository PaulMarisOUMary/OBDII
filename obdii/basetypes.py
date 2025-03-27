from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from re import findall
from time import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


class Mode(Enum):
    NONE = ''
    """Special mode used for the REPEAT command"""

    AT = "AT"
    """Special mode to send AT commands"""

    REQUEST = 0x01
    """Request current data"""
    FREEZE_FRAME = 0x02
    """Request freeze frame data"""
    STATUS_DTC = 0x03
    """Request stored DTCs (Diagnostic Trouble Codes)"""
    CLEAR_DTC = 0x04
    """Clear/reset DTCs (Diagnostic Trouble Codes)"""
    O2_SENSOR = 0x05
    """Request oxygen sensor monitoring test results"""
    PENDING_DTC = 0x06
    """Request DTCs (Diagnostic Trouble Codes) pending"""
    CONTROL_MODULE = 0x07
    """Request control module information"""
    O2_SENSOR_TEST = 0x08
    """Request oxygen sensor test results"""
    VEHICLE_INFO = 0x09
    """Request vehicle information"""
    PERMANENT_DTC = 0x0A
    """Request permanent DTCs (Diagnostic Trouble Codes)"""


class Protocol(Enum):
    UNKNOWN = -1
    """Unknown protocol"""

    AUTO = 0x00
    """Automatically determine the protocol"""
    SAE_J1850_PWM = 0x01
    """SAE J1850 PWM (41.6 kbaud)"""
    SAE_J1850_VPW = 0x02
    """SAE J1850 VPW (10.4 kbaud)"""
    ISO_9141_2 = 0x03
    """ISO 9141-2 (5 baud init, 10.4 kbaud)"""
    ISO_14230_4_KWP = 0x04
    """ISO 14230-4 KWP (5 baud init, 10.4 kbaud)"""
    ISO_14230_4_KWP_FAST = 0x05
    """ISO 14230-4 KWP (fast init, 10.4 kbaud)"""
    ISO_15765_4_CAN = 0x06
    """ISO 15765-4 CAN (11 bit ID, 500 kbaud)"""
    ISO_15765_4_CAN_B = 0x07
    """ISO 15765-4 CAN (29 bit ID, 500 kbaud)"""
    ISO_15765_4_CAN_C = 0x08
    """ISO 15765-4 CAN (11 bit ID, 250 kbaud)"""
    ISO_15765_4_CAN_D = 0x09
    """ISO 15765-4 CAN (29 bit ID, 250 kbaud)"""
    SAE_J1939_CAN = 0x0A
    """SAE J1939 CAN (29 bit ID, 250* kbaud) *default settings (user adjustable)"""
    USER1_CAN = 0x0B
    """USER1 CAN (11* bit ID, 125* kbaud) *default settings (user adjustable)"""
    USER2_CAN = 0x0C
    """USER2 CAN (11* bit ID, 50* kbaud) *default settings (user adjustable)"""


TNumeric = Union[int, float]

class Command():
    def __init__(self, 
            mode: Mode,
            pid: Union[int, str],
            n_bytes: int,
            name: str,
            description: Optional[str] = None,
            min_values: Optional[Union[TNumeric, List[TNumeric]]] = None,
            max_values: Optional[Union[TNumeric, List[TNumeric]]] = None,
            units: Optional[Union[str, List[str]]] = None,
            formula: Optional[Callable] = None,
            command_args: Optional[Dict[str, Any]] = None,
        ) -> None:
        self.mode = mode
        self.pid = pid
        self.n_bytes = n_bytes
        self.name = name
        self.description = description
        self.min_values = min_values
        self.max_values = max_values
        self.units = units
        self.formula = formula

        self.command_args = command_args or {}
        self.is_formatted = False

    def __call__(self, *args: Any, checks: bool = True) -> "Command":
        expected_args = len(self.command_args)

        if not expected_args:
            raise ValueError(f"Command '{self.__repr__()}' should not be parametrized, as no arguments has been described")

        received_args = len(args)
        if expected_args != received_args:
            raise ValueError(f"{self.__repr__()} expects {expected_args} argument(s), but got {received_args}")

        actual_placeholders = set(findall(r"{(\w+)}", str(self.pid)))
        expected_placeholders = set(self.command_args.keys())

        if actual_placeholders != expected_placeholders:
            missing = expected_placeholders - actual_placeholders
            extra = actual_placeholders - expected_placeholders
            raise ValueError(f"PID format mismatch. Missing placeholders: {missing}. Extra placeholders: {extra}")
        
        fmt_command = deepcopy(self)
        combined_args = {}
        try:
            for (arg_name, arg_type), value in zip(self.command_args.items(), args):
                if checks:
                    if not isinstance(value, arg_type):
                        raise TypeError(f"Argument '{arg_name}' must be of type {arg_type}, but got {type(value).__name__}")

                    arg_len = len(arg_name)
                    if isinstance(value, int):
                        if value < 0:
                            raise ValueError(f"Argument '{arg_name}' cannot be negative (got {value}).")
                        formatted_value = f"{value:0{arg_len}X}"

                        if len(formatted_value) > arg_len:
                            raise ValueError(f"Formatted value '{formatted_value}' exceeds expected length {len(arg_name)} for argument '{arg_name}'")
                        value = formatted_value

                    elif isinstance(value, str) and len(value) != arg_len:
                        raise ValueError(f"Argument '{arg_name}' should have length {arg_len}, but got {len(value)}")

                combined_args[arg_name] = value

            fmt_command.is_formatted = True
            fmt_command.pid = str(self.pid).format(**combined_args)
        except Exception as e:
            raise e

        return fmt_command

    def __repr__(self) -> str:
        return f"<Command {self.mode} {self.pid if isinstance(self.pid, str) else f'{self.pid:02X}'} {self.name or 'Unnamed'} [{', '.join(self.command_args.keys())}]>"
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Command):
            return False

        return vars(self) == vars(value)

    def build(self) -> bytes:
        """Builds the query to be sent.
        ELM327 is not case-sensitive, ignores spaces and all control characters."""
        if self.command_args and not self.is_formatted:
            raise ValueError(f"Command has unset arguments for '{self.pid}': {self.command_args}")

        mode = self.mode.value
        pid = self.pid
        if isinstance(mode, int):
            mode = f"{mode:02X}"
        if isinstance(pid, int):
            pid = f"{pid:02X}"
        return f"{mode} {pid}\r".encode() # \r ends each command


class BaseMode():
    def __getitem__(self, key) -> Command:
        if isinstance(key, int):
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if hasattr(attr, "pid") and attr.pid == key:
                    return attr
        raise KeyError(f"No command found with PID {key}")
    
    def __repr__(self) -> str:
        return f"<Mode Commands: {len(self)}>"

    def __len__(self) -> int:
        return len([1 for attr_name in dir(self) if isinstance(getattr(self, attr_name), Command)])
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseMode):
            return False
        
        return vars(self) == vars(value)
    
    def has_command(self, command: Union[Command, str]) -> bool:
        if isinstance(command, Command):
            command = command.name

        command = command.upper()
        return hasattr(self, command) and isinstance(getattr(self, command), Command)

@dataclass
class Context():
    command: Command
    protocol: Protocol
    timestamp: float = field(default_factory=time)

@dataclass
class BaseResponse():
    context: Context
    raw: bytes
    messages: List[bytes]
    timestamp: float = field(default_factory=time)

T_Parsed_Data = List[Tuple[bytes, ...]]

@dataclass
class Response(BaseResponse):
    parsed_data: Optional[T_Parsed_Data] = None

    value: Optional[Any] = None

    @property
    def min_values(self) -> Optional[Union[TNumeric, List[TNumeric]]]:
        return self.context.command.min_values
    
    @property
    def max_values(self) -> Optional[Union[TNumeric, List[TNumeric]]]:
        return self.context.command.max_values
    
    @property
    def units(self) -> Optional[Union[str, List[str]]]:
        return self.context.command.units
