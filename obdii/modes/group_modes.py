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
            item = getattr(self, key, None)
            if not isinstance(item, Command):
                raise KeyError(f"Command '{key}' not found")
            return item
        elif isinstance(key, int):
            mode = self.modes.get(key)
            if not isinstance(mode, GroupCommands):
                raise KeyError(f"Mode '{key}' not found")
            return mode

        raise TypeError(f"Invalid key type: {type(key)}. Expected str or int.")