from typing import Union

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
