from typing import Dict, Union

from .mode_01 import Mode01
from .mode_02 import Mode02
from .mode_03 import Mode03
from .mode_04 import Mode04

from .mode_09 import Mode09


ModesType = Union[
    Mode01, 
    Mode02,
    Mode03,
    Mode04,

    Mode09,
    ]

class Modes(
    Mode01,
    Mode02,
    Mode03,
    Mode04,

    Mode09,
    ): ...

MODE_REGISTRY: Dict[int, ModesType] = {
    0x01: Mode01(),
    0x02: Mode02(),
    0x03: Mode03(),
    0x04: Mode04(),

    0x09: Mode09(),
}