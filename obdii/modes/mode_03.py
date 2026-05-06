from functools import partial

from .group_commands import GroupCommands

from ..command import Command
from ..mode import Mode
from ..parsers.dtc import DTC


M = Mode.STATUS_DTC
C = partial(Command, M)

# https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_03_-_Show_stored_Diagnostic_Trouble_Codes_(DTCs)


class Mode03(GroupCommands, registry_id=M):
    """Get Diagnostic Trouble Codes Command"""

    GET_DTC = C('', resolver=DTC.parse)
    """Request Diagnostic Trouble Codes (DTCs)"""
