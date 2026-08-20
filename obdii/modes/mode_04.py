from ..command import Command
from ..mode import Mode
from .group_commands import GroupCommands

M = Mode.CLEAR_DTC
C = Command

# https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_04_-_Clear_Diagnostic_Trouble_Codes_and_stored_values

class Mode04(GroupCommands, registry_id=M):
    """Clear Diagnostic Trouble Codes Command"""

    CLEAR_DTC = C(M, '')
    """Clear Diagnostic Trouble Codes / Malfunction indicator lamp (MIL) / Check engine light and Freeze frame data"""