from typing import Optional, ClassVar, Dict, Union, Iterator

from ..command import Command

from .basetypes import CommandKey, RegistryKey


class GroupCommands:
    """Single-mode command container.

    Subclassed by each mode, see ``mode_**.py``.

    Access syntax:
        - ``group.ENGINE_SPEED`` -- by attribute -> :class:`Command`
        - ``group["ENGINE_SPEED"]`` -- by name -> :class:`Command`
        - ``group[0x0C]`` -- by PID -> :class:`Command`

    Indexes are built once per instance by scanning the instance's attributes.
    """

    _registry_id: ClassVar[RegistryKey]

    def __init_subclass__(
        cls, /, registry_id: Optional[RegistryKey] = None, **kwargs
    ) -> None:
        super().__init_subclass__(**kwargs)

        if registry_id is not None:
            cls._registry_id = registry_id

    def __init__(self) -> None:
        self.by_pid: Dict[int, Command] = {}
        self.by_name: Dict[str, Command] = {}

        for name in dir(self):
            if name.startswith('_'):
                continue

            attr = getattr(self, name, None)
            if not isinstance(attr, Command):
                continue

            if isinstance(attr.pid, int):
                self.by_pid[attr.pid] = attr
            self.by_name[attr.name.upper()] = attr

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {len(self)}>"

    def __iter__(self) -> Iterator[Command]:
        return iter(self.by_name.values())

    def __len__(self) -> int:
        return len(self.by_name)

    def __contains__(self, item: Union[Command, str]) -> bool:
        if isinstance(item, Command):
            return self.by_name.get(item.name.upper()) is item
        return item.upper() in self.by_name

    def __getitem__(self, key: CommandKey) -> Command:
        if isinstance(key, str):
            try:
                return self.by_name[key.upper()]
            except KeyError:
                raise KeyError(f"Command '{key}' not found") from None
        elif isinstance(key, int):
            try:
                return self.by_pid[key]
            except KeyError:
                raise KeyError(f"No command found with PID {key}") from None

        raise TypeError(f"Invalid key type: {type(key)}")
