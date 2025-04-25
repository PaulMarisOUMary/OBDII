from enum import Enum


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