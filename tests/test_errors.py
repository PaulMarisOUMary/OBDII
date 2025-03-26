import pytest

from obdii.errors import (
    BaseResponseError, 
    UnknownCommandError, BufferFullError, BusBusyError, BusError, 
    CanError, DataError, DataPointError, ErrxxError, FeedbackError, 
    NoDataError, RxError, StoppedError, ConnectionFailureError,
    InactivityWarning, LowPowerWarning, LowVoltageResetWarning,
)


@pytest.mark.parametrize(
    "response, expected_error",
    [
        (b'?', UnknownCommandError),
        (b"BUFFER FULL", BufferFullError),
        (b"BUS BUSY", BusBusyError),
        (b"BUS ERROR", BusError),
        (b"CAN ERROR", CanError),
        (b"DATA ERROR", DataError),
        (b"SOME DATA ERROR", DataError),
        (b"<DATA ERROR", DataPointError),
        (b"SOME <DATA ERROR", DataPointError),
        (b"ERR01", ErrxxError),
        (b"ERR99", ErrxxError),
        (b"FB ERROR", FeedbackError),
        (b"NO DATA", NoDataError),
        (b"<RX ERROR", RxError),
        (b"STOPPED", StoppedError),
        (b"UNABLE TO CONNECT", ConnectionFailureError),

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