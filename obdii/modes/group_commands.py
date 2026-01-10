from typing import Generator, Optional, Union

from ..command import Command
from ..mode import Mode


class GroupCommands:
    def __init_subclass__(
        cls, /, registry_id: Optional[Union[Mode, int]] = None, **kwargs
    ) -> None:
        super().__init_subclass__(**kwargs)

        if registry_id is not None:
            cls._registry_id = Mode.get_from(registry_id, default=registry_id)

    def __getitem__(self, key: Union[int, str]) -> Command:
        if isinstance(key, str):
            key = key.upper()
            item = getattr(self, key, None)
            if not isinstance(item, Command):
                raise KeyError(f"Command '{key}' not found")
            return item
        elif isinstance(key, int):
            for cmd in self:
                if cmd.pid == key:
                    return cmd
            raise KeyError(f"No command found with PID {key}")

        raise TypeError(f"Invalid key type: {type(key)}")

    def __iter__(self) -> Generator[Command, None, None]:
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue
            attr = getattr(self, attr_name)
            if isinstance(attr, Command):
                yield attr

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {len(self)}>"

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __contains__(self, item: Union[Command, str]) -> bool:
        if isinstance(item, Command):
            return any(item is cmd for cmd in self)
        return isinstance(getattr(self, item.upper(), None), Command)
