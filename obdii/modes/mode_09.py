from functools import partial

from .group_commands import GroupCommands

from ..command import Command
from ..mode import Mode
from ..parsers.pids import SupportedPIDS


M = Mode.VEHICLE_INFO
C = partial(Command, M)
SP = SupportedPIDS

# https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_09_-_Request_vehicle_information

class Mode09(GroupCommands, registry_id=M):
    """Request Vehicle Information"""

    SUPPORTED_PIDS_9 = C(0x00, 0x04, resolver=SP(0x01))
    """Service 9 supported PIDs [$01 to $20]"""
    VIN_MESSAGE_COUNT = C(0x01, 0x01)
    """VIN Message Count in PID 02. Only for ISO 9141-2, ISO 14230-4 and SAE J1850."""
    VIN = C(0x02, 0x11)
    """Vehicle Identification Number (VIN)"""
    CALIBRATION_ID_MESSAGE_COUNT = C(0x03, 0x01)
    """Calibration ID message count for PID 04. Only for ISO 9141-2, ISO 14230-4 and SAE J1850."""
    CALIBRATION_ID = C(0x04, [16, 32, 48, 64])
    """Calibration ID"""
    CVN_MESSAGE_COUNT = C(0x05, 0x01)
    """Calibration verification numbers (CVN) message count for PID 06. Only for ISO 9141-2, ISO 14230-4 and SAE J1850."""
    CVN = C(0x06, [4, 8, 12, 16])
    """Calibration Verification Numbers (CVN) Several CVN can be output (4 bytes each) the number of CVN and CALID must match"""
    IN_USE_PERF_TRACKING_MESSAGE_COUNT = C(0x07, 0x01, min_values=8, max_values=10)
    """In-use performance tracking message count for PID 08 and 0A. Only for ISO 9141-2, ISO 14230-4 and SAE J1850."""
    IN_USE_PERF_TRACKING_SPARK_IGNITION = C(0x08, 0x04)
    """In-use performance tracking for spark ignition vehicles"""
    ECU_NAME_MESSAGE_COUNT = C(0x09, 0x01)
    """ECU name message count for PID 0A"""
    ECU_NAME = C(0x0A, 0x14)
    """ECU name"""
    IN_USE_PERF_TRACKING_COMPRESSION_IGNITION = C(0x0B, 0x04)
    """In-use performance tracking for compression ignition vehicles"""