from typing import Dict, Union

from .modeat import ModeAT

from .mode01 import Mode01
from .mode02 import Mode02
from .mode03 import Mode03
from .mode04 import Mode04

# Initialize AT Commands
at_commands = ModeAT()

__all__ = [
    "at_commands",
    "Modes",
    "T_Modes",
    "d_modes",
    "ModeAT",
    "Mode01",
    "Mode02",
    "Mode03",
    "Mode04",
]

T_Modes = Union[
    Mode01, 
    Mode02,
    Mode03,
    Mode04,
    ]

d_modes: Dict[int, T_Modes] = {
    0x01: Mode01(),
    0x02: Mode02(),
    0x03: Mode03(),
    0x03: Mode04(),
}

class Modes(
    Mode01,
    Mode02,
    Mode03,
    Mode04,
    ): ...