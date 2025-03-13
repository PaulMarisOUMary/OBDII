import time

from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional, Union


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

    def __repr__(self) -> str:
        return f"<Mode {self.name} ({self.value if isinstance(self.value, str) else f'{self.value:02X}'})>"
    
    def __str__(self) -> str:
        return self.__repr__()


class Command():
    def __init__(self, 
            mode: Mode,
            pid: Union[int, str],
            n_bytes: int,
            name: str,
            description: Optional[str] = None,
            min_value: Optional[Union[int, float, str]] = None,
            max_value: Optional[Union[int, float, str]] = None,
            units: Optional[str] = None,
            command_args: Optional[Dict[str, Any]] = None,
        ) -> None:
        self.mode = mode
        self.pid = pid
        self.n_bytes = n_bytes
        self.name = name
        self.description = description
        self.min_value = min_value
        self.max_value = max_value
        self.units = units
        self.command_args = command_args or {}

    def __call__(self, *args: Any, checks: bool = True) -> "Command":
        if not self.command_args or not args or len(self.command_args) != len(args):
            raise TypeError(f"{self.__repr__()} expects {len(self.command_args)} argument(s), but got {len(args)}")

        try:
            combined_args = {}
            for (arg, arg_type), value in zip(self.command_args.items(), args):
                if checks:
                    if not isinstance(value, arg_type):
                        raise TypeError(f"Argument '{arg}' should be of type {arg_type}")

                    if isinstance(value, int):
                        value = f"{value:0{len(arg)}d}"
                    elif isinstance(value, str) and len(value) != len(arg):
                        raise ValueError(f"Argument '{arg}' should have length {len(arg)}, but got {len(value)}")

                combined_args[arg] = value

            self.pid = str(self.pid).format(**combined_args)
        except Exception as e:
            raise e
        return self

    def __repr__(self) -> str:
        return f"<Command {self.mode} {self.pid if isinstance(self.pid, str) else f'{self.pid:02X}'} {self.name or 'Unnamed'} [{', '.join(self.command_args.keys())}]>"
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Command):
            return False

        return (
            self.mode == value.mode and
            self.name == value.name and
            self.description == value.description and
            self.command_args == value.command_args
        )


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

    def __len__(self):
        return len([1 for attr_name in dir(self) if isinstance(getattr(self, attr_name), Command)])
    
    def has_command(self, command: Union[Command, str]) -> bool:
        if isinstance(command, Command):
            command = command.name

        command = command.upper()
        return hasattr(self, command) and isinstance(getattr(self, command), Command)


class BaseResponse(NamedTuple):
    command: Command
    raw_response: List[bytes]
    message: List[List[bytes]]
    timestamp: float = time.time()