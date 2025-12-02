from typing import Union, overload

from .basetypes import Modes, ModesType
from .group_commands import GroupCommands

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
    def __getitem__(self, key: Union[Mode, int]) -> ModesType: ...

    def __getitem__(self, key: Union[Mode, int, str]):
        if not isinstance(key, (Mode, int)):
            return super().__getitem__(key)

        mode = Mode.get_from(key, default=key)
        mode_key = self.modes.get(mode)
        if not isinstance(mode_key, GroupCommands):
            raise KeyError(f"Mode '{key}' not found")
        return mode_key