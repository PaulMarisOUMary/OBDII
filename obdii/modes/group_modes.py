from typing import Union, Literal, overload

from .basetypes import Modes, ModesType
from .group_commands import GroupCommands
from .mode_01 import Mode01
from .mode_02 import Mode02
from .mode_03 import Mode03
from .mode_04 import Mode04
from .mode_09 import Mode09

from ..command import Command
from ..mode import Mode


class GroupModes(Modes):
    def __init__(self):
        self.modes = {}
        for cls in Modes.mro():
            if issubclass(cls, GroupCommands) and "_registry_id" in cls.__dict__:
                self.modes[cls._registry_id] = cls()

    @overload
    def __getitem__(self, key: str) -> Command: ...

    @overload
    def __getitem__(self, key: Union[Literal[Mode.REQUEST], Literal[1]]) -> Mode01: ...

    @overload
    def __getitem__(
        self, key: Union[Literal[Mode.FREEZE_FRAME], Literal[2]]
    ) -> Mode02: ...

    @overload
    def __getitem__(
        self, key: Union[Literal[Mode.STATUS_DTC], Literal[3]]
    ) -> Mode03: ...

    @overload
    def __getitem__(
        self, key: Union[Literal[Mode.CLEAR_DTC], Literal[4]]
    ) -> Mode04: ...

    @overload
    def __getitem__(
        self, key: Union[Literal[Mode.VEHICLE_INFO], Literal[9]]
    ) -> Mode09: ...

    def __getitem__(self, key: Union[Mode, int, str]) -> Union[ModesType, Command]:  # type: ignore[invalid-method-override]
        if not isinstance(key, (Mode, int)):
            return super().__getitem__(key)

        mode = Mode.get_from(key, default=key)
        mode_key = self.modes.get(mode)
        if not isinstance(mode_key, GroupCommands):
            raise KeyError(f"Mode '{key}' not found")
        return mode_key
