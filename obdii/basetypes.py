from enum import Enum
from typing import Optional, TypedDict, Union


class Mode(Enum):
    AT = "AT"
    """Special mode to send AT commands"""

    REQUEST = 0x1
    """Request current data"""
    FREEZE_FRAME = 0x2
    """Request freeze frame data"""
    STATUS_DTC = 0x3
    """Request stored DTCs (Diagnostic Trouble Codes)"""
    CLEAR_DTC = 0x4
    """Clear/reset DTCs (Diagnostic Trouble Codes)"""
    O2_SENSOR = 0x5
    """Request oxygen sensor monitoring test results"""
    PENDING_DTC = 0x6
    """Request DTCs (Diagnostic Trouble Codes) pending"""
    CONTROL_MODULE = 0x7
    """Request control module information"""
    O2_SENSOR_TEST = 0x8
    """Request oxygen sensor test results"""
    VEHICLE_INFO = 0x9
    """Request vehicle information"""
    PERMANENT_DTC = 0xA
    """Request permanent DTCs (Diagnostic Trouble Codes)"""

    def __repr__(self) -> str:
        return f"<Mode {self.value:02X} {self.name.replace('_', ' ').title()}>"


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
    def __getitem__(self, key: int) -> object:
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, "pid") and attr.pid == key:
                return attr
        raise KeyError(f"No command found with PID {key}")
    
    def __repr__(self) -> str:
        return f"<Mode Commands: {len(self)}>" # type: ignore

    def __len__(self):
        return len([1 for attr_name in dir(self) if isinstance(getattr(self, attr_name), Command)])
