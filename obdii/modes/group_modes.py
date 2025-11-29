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
    def __getitem__(self, key: Union[int, Mode]) -> ModesType: ...

    def __getitem__(self, key: Union[str, int, Mode]):
        if not isinstance(key, (int, Mode)):
            return super().__getitem__(key)

        mode = self.modes.get(key.value if isinstance(key, Mode) else key)
        if not isinstance(mode, GroupCommands):
            raise KeyError(f"Mode '{key}' not found")
        return mode
