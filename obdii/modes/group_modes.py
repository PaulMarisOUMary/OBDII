from typing import Union, overload

from .basetypes import MODE_REGISTRY, Modes, ModesType
from .group_commands import GroupCommands

from ..command import Command


class GroupModes(Modes):
    def __init__(self):
        self.modes = MODE_REGISTRY

    @overload
    def __getitem__(self, key: str) -> Command: ...

    @overload
    def __getitem__(self, key: int) -> ModesType: ...

    def __getitem__(self, key: Union[str, int]):
        if isinstance(key, str):
            key = key.upper()
            if not key in dir(self):
                raise KeyError(f"Command '{key}' not found")
            item = getattr(self, key)
            if not isinstance(item, Command):
                raise TypeError(f"Expected Command but got {type(item)} for key '{key}'")
            return item
        elif isinstance(key, int):
            if not key in self.modes:
                raise KeyError(f"Mode '{key}' not found")
            mode = self.modes.get(key)
            if not isinstance(mode, GroupCommands):
                raise TypeError(f"Expected Mode but got {type(mode)} for key '{key}'")
            return mode