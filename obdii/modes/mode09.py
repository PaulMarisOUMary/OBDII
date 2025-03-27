from functools import partial

from ..basetypes import BaseMode, Command, Mode
from ..parser import SupportedPIDS

M = Mode.VEHICLE_INFO
C = partial(Command, M)
SP = SupportedPIDS

# https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_09_-_Request_vehicle_information

class Mode09(BaseMode):
    """Request Vehicle Information"""

    SUPPORTED_PIDS_9 = C(0x00, 0x04, "SUPPORTED_PIDS_9", "Service 9 supported PIDs [$01 to $20]", None, None, None, SP(0x01))
    VIN_MESSAGE_COUNT = C(0x01, 0x01, "VIN_MESSAGE_COUNT", "VIN Message Count in PID 02. Only for ISO 9141-2, ISO 14230-4 and SAE J1850.", None, None, None)
    VIN = C(0x02, 0x11, "VIN", "Vehicle Identification Number (VIN)", None, None, None)
    CALIBRATION_ID_MESSAGE_COUNT = C(0x03, 0x01, "CALIBRATION_ID_MESSAGE_COUNT", "Calibration ID message count for PID 04. Only for ISO 9141-2, ISO 14230-4 and SAE J1850.", None, None, None)
    CALIBRATION_ID = C(0x04, 0x00, "CALIBRATION_ID", "Calibration ID", None, None, None)
    CVN_MESSAGE_COUNT = C(0x05, 1, "CVN_MESSAGE_COUNT", "Calibration verification numbers (CVN) message count for PID 06. Only for ISO 9141-2, ISO 14230-4 and SAE J1850.", None, None, None)
    CVN = C(0x06, 0x00, "CVN", "Calibration Verification Numbers (CVN) Several CVN can be output (4 bytes each) the number of CVN and CALID must match", None, None, None)
    IN_USE_PERF_TRACKING_MESSAGE_COUNT = C(0x07, 0x01, "IN_USE_PERF_TRACKING_MESSAGE_COUNT", "In-use performance tracking message count for PID 08 and 0A. Only for ISO 9141-2, ISO 14230-4 and SAE J1850.", 8, 10, None)
    IN_USE_PERF_TRACKING_SPARK_IGNITION = C(0x08, 0x04, "IN_USE_PERF_TRACKING_SPARK_IGNITION", "In-use performance tracking for spark ignition vehicles", None, None, None)
    ECU_NAME_MESSAGE_COUNT = C(0x09, 0x01, "ECU_NAME_MESSAGE_COUNT", "ECU name message count for PID 0A", None, None, None)
    ECU_NAME = C(0x0A, 0x14, "ECU_NAME", "ECU name", None, None, None)
    IN_USE_PERF_TRACKING_COMPRESSION_IGNITION = C(0x0B, 0x04, "IN_USE_PERF_TRACKING_COMPRESSION_IGNITION", "In-use performance tracking for compression ignition vehicles", None, None, None)