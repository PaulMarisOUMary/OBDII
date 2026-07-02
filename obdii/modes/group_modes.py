from __future__ import annotations

from typing import Union, Dict, Iterator, overload, Literal, TYPE_CHECKING

from .basetypes import RegistryKey
from .group_commands import GroupCommands

from ..command import Command
from ..mode import Mode

if TYPE_CHECKING:
    from .mode_01 import Mode01
    from .mode_02 import Mode02
    from .mode_03 import Mode03
    from .mode_04 import Mode04
    from .mode_09 import Mode09


class GroupModes:
    """Group several :class:`GroupCommands` subclasses into one container.

    Not usable standalone: a concrete aggregate subclasses both this class and every :class:`GroupCommands`-based mode it wants to expose, see :class:`Modes`.

    Access syntax:
        - ``group.ENGINE_SPEED`` -- by attribute -> :class:`Command`
        - ``group["ENGINE_SPEED"]`` -- by name -> :class:`Command`
        - ``group[Mode.REQUEST]`` / ``group[1]`` -- by mode -> :class:`GroupCommands`

    Indexes are built once per instance by scanning the instance's attributes.
    """

    modes: Dict[RegistryKey, GroupCommands]

    def __init__(self) -> None:
        self.modes = {
            base._registry_id: base()
            for base in type(self).mro()
            if issubclass(base, GroupCommands)
            and "_registry_id" in base.__dict__
            and base._registry_id is not None
        }

        self.by_name = {}
        for name in dir(self):
            if name.startswith('_'):
                continue

            attr = getattr(self, name, None)
            if isinstance(attr, Command):
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

    def __getitem__(self, key: RegistryKey) -> Union[Command, GroupCommands]:
        if isinstance(key, str):
            try:
                return self.by_name[key.upper()]
            except KeyError:
                raise KeyError(f"Command '{key}' not found") from None
        elif isinstance(key, (Mode, int)):
            resolved = Mode.get_from(key, default=key)
            if isinstance(resolved, Mode) and resolved in self.modes:
                return self.modes[resolved]
            raise KeyError(f"Mode '{key}' not found")

        raise TypeError(f"Invalid key type: {type(key)}")
