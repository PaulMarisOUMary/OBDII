"""
Unit tests for obdii.errors module.
"""
import pytest

from obdii.errors import (
    ResponseBaseError,
    InvalidCommandError,
    BufferFullError,
    BusBusyError,
    BusError,
    CanError,
    InvalidDataError,
    InvalidLineError,
    DeviceInternalError,
    SignalFeedbackError,
    MissingDataError,
    CanDataError,
    StoppedError,
    ProtocolConnectionError,
    InactivityWarning,
    LowPowerWarning,
    LowVoltageResetWarning,
)


@pytest.mark.parametrize(
    ("response", "expected_error"),
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
    ],
    ids=[
        "invalid_cmd",
        "buffer_full",
        "bus_busy",
        "bus_error",
        "can_error",
        "data_error",
        "data_error_some",
        "invalid_line_lt",
        "invalid_line_some_lt",
        "device_err01",
        "device_err99",
        "fb_error",
        "no_data",
        "can_data_error",
        "stopped",
        "unable_connect",
        "inactivity",
        "low_power",
        "low_voltage_reset",
        "no_error",
    ],
)
def test_error_detection(response, expected_error):
    result = ResponseBaseError.detect(response)
    if expected_error is None:
        assert result is None, f"Expected no error but got {result}"
    else:
        assert isinstance(result, expected_error), f"Expected {expected_error.__name__}, but got {type(result).__name__}"