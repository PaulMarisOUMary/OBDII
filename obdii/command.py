from __future__ import annotations

from copy import deepcopy
from re import Match, Pattern, compile
from typing import Any, Callable, Dict, Optional, Tuple, Union

from .basetypes import MISSING, OneOrMany, Real
from .mode import Mode


class Template:
    """
    Represents a string template with named placeholders that can be substituted with values.

    The template definition uses curly braces `{}`, each placeholder follows the format `{name:type}`, where `name` is the parameter name and `type` is an optional type specifier.

    The following type specifiers are supported:
    - `str`: Converts the value to a string.
    - `int`: Converts the value to an integer.
    - `hexN`: Converts the value to a hexadecimal string, padded to N digits (e.g., `hex2` for 2 digits).

    Few rules and assumptions apply when defining and substituting templates:
    - Placeholder names must be unique within a template.
    - If a type specifier is not provided, the value will be treated as a string.
    - When substituting values, either positional or keyword arguments can be used, but not both.
    - If using positional arguments, the number of arguments must match the number of placeholders.
    - If using keyword arguments, all placeholder names must be provided.

    Example
    -------
    .. code-block:: python

        t = Template("AT {a:str} {b:int} {c:hex4} {d}")
        r = t.substitute(a=1, b=2.2, c=3, d="four")
        # or
        r = t.substitute(1, 2.2, 3, "four")

        >>> r
        "AT 1 2 0003 four"
    """

    PARAM_RE = compile(r"\{\s*(?P<name>\w+)\s*(?::\s*(?P<type>\w+))?\s*\}")
    HEX_RE = compile(r"hex(?P<width>\d*)")

    TYPE_MAP: Dict[Union[str, Pattern], Callable[[Dict, Any], str]] = {
        "str": lambda _, v: f"{v}",
        "int": lambda _, v: f"{int(v)}",
        HEX_RE: lambda m, v: format(int(v), f"0{m.get('width') or '1'}X"),
    }

    def __init__(self, template: str) -> None:
        self.template = template

        self.params = [
            {
                **match.groupdict(),
                "placeholder": match.group(0),
            }
            for match in self.PARAM_RE.finditer(template)
        ]

        self.template_names = [param["name"] for param in self.params]

        if len(self.params) != len(set(self.template_names)):
            raise ValueError("Duplicate parameter names in template.")

    def __repr__(self) -> str:
        return f'<Template "{self.template}" {self.template_names}>'

    def _cast(
        self, param_type: Union[str, Pattern]
    ) -> Tuple[Dict, Callable[[Dict, Any], str]]:
        cast_fn = self.TYPE_MAP.get(param_type)
        if cast_fn:
            return {}, cast_fn

        for pattern, fn in self.TYPE_MAP.items():
            if isinstance(pattern, Pattern):
                match = pattern.fullmatch(param_type)
                if match:
                    return match.groupdict(), fn

        raise ValueError(f"Unsupported type specifier: {param_type}.")

    def substitute(self, *args, **kwargs) -> str:
        """
        Substitute the placeholders in the template with the provided values.

        The substitution must use either positional or keyword arguments, not both.

        Parameters
        ----------
        *args: :class:`Any`
            Positional arguments corresponding to the placeholders in the template.
        **kwargs: :class:`Any`
            Keyword arguments corresponding to the placeholders in the template.

        Returns:
            str: The template string with placeholders replaced by the provided values.
        """
        if args and kwargs:
            raise ValueError("Cannot use both positional and keyword arguments.")

        if args:
            if len(args) != len(self.params):
                raise ValueError(
                    "Number of positional arguments does not match number of parameters."
                )
            values = {param["name"]: arg for param, arg in zip(self.params, args)}
        else:
            arg_names = set(kwargs)
            diff = set(self.template_names) ^ arg_names

            if diff:
                raise ValueError(
                    f"Parameters and arguments do not match template signature: {self.template_names} got {arg_names}."
                )
            values = kwargs

        def replace_placeholder(match: Match[str]) -> str:
            name = match.group("name")
            param_type = match.group("type") or "str"

            if name not in values:
                raise ValueError(f"Missing argument for placeholder: {name}.")

            value = values[name]
            match_dict, cast_fn = self._cast(param_type)

            return cast_fn(match_dict, value)

        result, n_replaced = self.PARAM_RE.subn(replace_placeholder, self.template)
        if n_replaced != len(self.params):
            raise ValueError(
                f"Placeholder(s) got replaced incorrectly. Expected {len(self.params)}, got {n_replaced}."
            )

        return result


class Command:
    def __init__(
        self,
        mode: Union[Mode, int, str],
        pid: Union[Template, int, str],
        expected_bytes: OneOrMany[int] = 0,
        min_values: Optional[OneOrMany[Real]] = MISSING,
        max_values: Optional[OneOrMany[Real]] = MISSING,
        units: Optional[OneOrMany[str]] = MISSING,
        resolver: Optional[Callable] = MISSING,
    ) -> None:
        """
        Initialize a Command instance.

        Parameters
        ----------
        mode: Union[:class:`Mode`, :class:`int`, :class:`str`]
            Command mode to be used.
        pid: Union[:class:`Template`, :class:`int`, :class:`str`]
            Command PID (Parameter Identifier) to be used.
        expected_bytes: OneOrMany[int]
            The number of bytes expected in the response.
        min_values: Optional[OneOrMany[Real]]
            Minimum valid values for the command's parameters.
        max_values: Optional[OneOrMany[Real]]
            Maximum valid values for the command's parameters.
        units: Optional[OneOrMany[str]]
            The units for the command's response.
        resolver: Optional[Callable]
            A resolver function for custom response handling.
        """
        self.mode = Mode.get_from(mode, default=mode)
        self.pid = pid
        self.expected_bytes = expected_bytes
        self.min_values = min_values
        self.max_values = max_values
        self.units = units
        self.resolver = resolver

        self.name = "Unnamed"

    def __set_name__(self, _: type, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Command {self.mode} {self.pid} {self.name}>"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Command):
            return False

        return self.mode == value.mode and self.pid == value.pid

    def __hash__(self) -> int:
        return hash((self.mode, self.pid))

    def __call__(self, *args, **kwargs) -> Command:
        """
        Formats the command with the provided positional or keyword arguments.

        Parameters
        ----------
        *args: :class:`Any`
            Positional arguments corresponding to placeholders in the command's PID template.
        **kwargs: :class:`Any`
            Keyword arguments corresponding to placeholders in the command's PID template.

        Returns
        -------
        :class:`Command`
            A new Command instance with the formatted PID.
        """
        if not isinstance(self.pid, Template):
            raise TypeError("Cannot format command with non-template PID.")

        fmt_command = deepcopy(self)
        fmt_command.pid = self.pid.substitute(*args, **kwargs)

        return fmt_command

    def _format_to_hex(self, value: Union[Mode, int, str]) -> str:
        if isinstance(value, Mode):
            value = value.value
        return f"{value:02X}" if isinstance(value, int) else value

    def _return_digit(self, early_return: bool) -> str:
        """Return hex digit for expected response lines (early-return ELM327 DSL, page 34)."""
        if not (
            early_return
            and self.expected_bytes
            and isinstance(self.expected_bytes, int)
            and Mode.get_from(self.mode) != Mode.AT
        ):
            return ''

        data_bytes = 7
        n_lines = (self.expected_bytes + (data_bytes - 1)) // data_bytes

        return f"{n_lines:X}" if 0 < n_lines < 16 else ''

    def build(self, early_return: bool = False) -> bytes:
        """
        Builds the query to be sent to the ELM327 device as a byte string.
        (The ELM327 is case-insensitive, ignores spaces and all control characters.)

        Parameters
        ----------
        early_return: :class:`bool`
            Whether to include the early return digit in the command.
            If set to `True`, appends a hex digit representing the expected number of responses in the query.
            Defaults to `False`.

        Returns
        -------
        :class:`bytes`
            The formatted query as a byte string, ready to be sent to the ELM327 device.

        Raises
        ------
        ValueError
            If the PID is a Template, which means your command has likely not been formatted.
        """
        if isinstance(self.pid, Template):
            raise ValueError("Cannot build command with unformatted PID template.")

        mode = self._format_to_hex(self.mode)
        pid = self._format_to_hex(self.pid)
        return_digit = self._return_digit(early_return)

        payload = f"{mode} {pid} {return_digit}".strip()
        query = f"{payload}\r"

        return query.encode()
