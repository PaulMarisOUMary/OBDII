from enum import Enum
from typing import Optional, TypedDict, Union


class Mode(Enum):
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
        return f"<Mode {self.name} {self.value if isinstance(self.value, str) else self.value:02X}>"


class Command():
    def __init__(self, 
            mode: Mode,
            pid: Union[int, str],
            n_bytes: int,
            name: str,
            description: Optional[str] = None,
            min_value: Optional[Union[int, float, str]] = None,
            max_value: Optional[Union[int, float, str]] = None,
            units: Optional[str] = None
        ) -> None:
        self.mode = mode
        self.pid = pid
        self.n_bytes = n_bytes
        self.name = name
        self.description = description
        self.min_value = min_value
        self.max_value = max_value
        self.units = units

    def __repr__(self) -> str:
        return f"<Command {self.mode} {self.pid:02X} {self.name or 'Unnamed'}>"


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
