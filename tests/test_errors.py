import pytest

from obdii.errors import (
    BaseResponseError, 
    InvalidCommandError, BufferFullError, BusBusyError, BusError, 
    CanError, InvalidDataError, InvalidLineError, DeviceInternalError, SignalFeedbackError, 
    MissingDataError, CanDataError, StoppedError, ProtocolConnectionError,
    InactivityWarning, LowPowerWarning, LowVoltageResetWarning,
)


@pytest.mark.parametrize(
    "response, expected_error",
    [
        (b'?', InvalidCommandError),
        (b"BUFFER FULL", BufferFullError),
        (b"BUS BUSY", BusBusyError),
        (b"BUS ERROR", BusError),
        (b"CAN ERROR", CanError),
        (b"DATA ERROR", InvalidDataError),
        (b"SOME DATA ERROR", InvalidDataError),
        (b"<DATA ERROR", InvalidLineError),
        (b"SOME <DATA ERROR", InvalidLineError),
        (b"ERR01", DeviceInternalError),
        (b"ERR99", DeviceInternalError),
        (b"FB ERROR", SignalFeedbackError),
        (b"NO DATA", MissingDataError),
        (b"<RX ERROR", CanDataError),
        (b"STOPPED", StoppedError),
        (b"UNABLE TO CONNECT", ProtocolConnectionError),

        (b"ACT ALERT", InactivityWarning),
        (b"LP ALERT", LowPowerWarning),
        (b"LV RESET", LowVoltageResetWarning),

        (b"NO ERROR HERE", None),
    ]
)
def test_error_detection(response, expected_error):
    error = BaseResponseError.detect(response)
    if expected_error is None:
        assert error is None, f"Expected no error but got {error}"
    else:
        assert isinstance(error, expected_error), f"Expected {expected_error.__name__}, but got {type(error).__name__}"