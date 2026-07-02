from typing import Union, TypeAlias, TYPE_CHECKING

from ..mode import Mode

if TYPE_CHECKING:
    from .mode_01 import Mode01
    from .mode_02 import Mode02
    from .mode_03 import Mode03
    from .mode_04 import Mode04

    from .mode_09 import Mode09


CommandKey: TypeAlias = Union[int, str]
RegistryKey: TypeAlias = Union[Mode, int, str]

ModesType: TypeAlias = Union["Mode01", "Mode02", "Mode03", "Mode04", "Mode09"]
