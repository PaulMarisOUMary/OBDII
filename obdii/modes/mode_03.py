from functools import partial

from .group_commands import GroupCommands

from ..command import Command
from ..mode import Mode


M = Mode.STATUS_DTC
C = partial(Command, M)

# https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_03_-_Show_stored_Diagnostic_Trouble_Codes_(DTCs)

class Mode03(GroupCommands):
    """Get Diagnostic Trouble Codes Command"""
    GET_DTC = C('', 0x00, "GET_DTC", "Request trouble codes", None, None, None)