from typing import Final

from .group_modes import GroupModes
from .mode_01 import Mode01
from .mode_02 import Mode02
from .mode_03 import Mode03
from .mode_04 import Mode04
from .mode_09 import Mode09
from .mode_at import ModeAT


class Modes(
    GroupModes,
    Mode01,
    Mode02,
    Mode03,
    Mode04,
    Mode09,
):
    """The concrete, top-level aggregate of every standard OBD mode."""


at_commands: Final[ModeAT] = ModeAT()
commands: Final[Modes] = Modes()


__all__ = [
    "Mode01",
    "Mode02",
    "Mode03",
    "Mode04",
    "Mode09",
    "ModeAT",
    "at_commands",
    "commands",
]
