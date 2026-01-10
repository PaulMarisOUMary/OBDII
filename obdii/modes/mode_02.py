from copy import deepcopy

from .group_commands import GroupCommands
from .mode_01 import Mode01

from ..command import Command
from ..mode import Mode


M = Mode.FREEZE_FRAME

# https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_02_-_Show_freeze_frame_data


class Mode02(GroupCommands, registry_id=M):
    """Freeze frame Commands"""

    @classmethod
    def _populate_commands(cls):
        for field_name, command in vars(Mode01).items():
            if isinstance(command, Command):
                field = f"DTC_{field_name}"
                dtc_command = deepcopy(command)
                dtc_command.mode = M
                dtc_command.name = field
                setattr(Mode02, field, dtc_command)


Mode02._populate_commands()
