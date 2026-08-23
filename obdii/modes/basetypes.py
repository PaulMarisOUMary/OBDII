from typing import TYPE_CHECKING, Union

from ..mode import Mode

if TYPE_CHECKING:
    from .mode_01 import Mode01
    from .mode_02 import Mode02
    from .mode_03 import Mode03
    from .mode_04 import Mode04
    from .mode_09 import Mode09


CommandKey = Union[int, str]
RegistryKey = Union[Mode, int, str]

ModesType = Union["Mode01", "Mode02", "Mode03", "Mode04", "Mode09"]
