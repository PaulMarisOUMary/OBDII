from typing import Dict, Union

from .modeat import ModeAT

from .mode01 import Mode01

# Initialize AT Commands
at_commands = ModeAT()

__all__ = [
    "at_commands",
    "Modes",
    "T_Modes",
    "d_modes",
    "ModeAT",
    "Mode01",
]

T_Modes = Union[Mode01]

d_modes: Dict[int, T_Modes] = {
    0x01: Mode01(),
}

class Modes(
    Mode01, 
    ): ...