from typing import overload

from .basetypes import Command

from .modes.mode01 import Mode01

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
    def __getitem__(self, key: int) -> Modes: ...

    def __getitem__(self, key): # type: ignore
        if isinstance(key, str):
            key = key.upper()
            if not key in dir(self):
                raise KeyError(f"Command '{key}' not found")
            item = getattr(self, key)
            if not isinstance(item, Command):
                raise TypeError(f"Expected Command but got {type(item)} for key '{key}'")
            return item
        elif isinstance(key, int):
            if key in self.modes:
                return self.modes.get(key)
            else:
                raise KeyError(f"Mode '{key}' not found")
        else:
            raise TypeError(f"Unsupported {type(key)} type")

# Initialize Commands
commands = Commands()