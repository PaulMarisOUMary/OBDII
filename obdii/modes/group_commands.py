from typing import Union

from ..command import Command


class GroupCommands():
    def __getitem__(self, key) -> Command:
        if isinstance(key, int):
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if hasattr(attr, "pid") and attr.pid == key:
                    return attr
        raise KeyError(f"No command found with PID {key}")

    def __repr__(self) -> str:
        return f"<Mode Commands: {len(self)}>"

    def __len__(self) -> int:
        return len([1 for attr_name in dir(self) if isinstance(getattr(self, attr_name), Command)])

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, GroupCommands):
            return False
        
        return vars(self) == vars(value)
    
    def has_command(self, command: Union[Command, str]) -> bool:
        if isinstance(command, Command):
            command = command.name

        command = command.upper()
        return hasattr(self, command) and isinstance(getattr(self, command), Command)