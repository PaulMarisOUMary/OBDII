from typing import Union, overload

from .basetypes import BaseMode, Command

from .modes import Mode01

T_Modes = Union[Mode01]

class Modes(
    Mode01, 
    ):
    pass

class Commands(Modes):
    def __init__(self):
        self.modes = {
            0x01: Mode01(),
        }

    @overload
    def __getitem__(self, key: str) -> Command: ...

    @overload
    def __getitem__(self, key: int) -> T_Modes: ...

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
            if not isinstance(mode, BaseMode):
                raise TypeError(f"Expected Mode but got {type(mode)} for key '{key}'")
            return mode
        else:
            raise TypeError(f"Unsupported {type(key)} type")

# Initialize Commands
commands = Commands()