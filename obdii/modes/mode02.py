from copy import deepcopy

from ..basetypes import BaseMode, Command, Mode

from .mode01 import Mode01


# https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_02_-_Show_freeze_frame_data

class Mode02(BaseMode):
    """Freeze frame Commands"""

    @classmethod
    def _populate_commands(cls):
        for field_name, command in Mode01.__dict__.items():
            if isinstance(command, Command):
                field = f"DTC_{field_name}"
                dtc_command = deepcopy(command)
                dtc_command.mode = Mode.FREEZE_FRAME
                dtc_command.name = field
                setattr(Mode02, field, dtc_command)

Mode02._populate_commands()