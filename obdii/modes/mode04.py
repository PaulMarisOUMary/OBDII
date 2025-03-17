from functools import partial

from ..basetypes import BaseMode, Command, Mode


M = Mode.CLEAR_DTC
C = partial(Command, M)

# https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_04_-_Clear_Diagnostic_Trouble_Codes_and_stored_values

class Mode04(BaseMode):
    """Clear Diagnostic Trouble Codes Command"""
    CLEAR_DTC = C('', 0x00, "CLEAR_DTC", "Clear trouble codes / Malfunction indicator lamp (MIL) / Check engine light", None, None, None)