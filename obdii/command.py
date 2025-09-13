from __future__ import annotations

from copy import deepcopy
from re import findall
from typing import Any, Callable, Dict, Optional, Union

from .basetypes import MISSING, OneOrMany, Real
from .mode import Mode


class Command:
    def __init__(
        self,
        mode: Mode,
        pid: Union[int, str],
        n_bytes: int,
        name: str,
        description: str = MISSING,
        min_values: Optional[OneOrMany[Real]] = MISSING,
        max_values: Optional[OneOrMany[Real]] = MISSING,
        units: Optional[OneOrMany[str]] = MISSING,
        formula: Optional[Callable] = MISSING,
        command_args: Optional[Dict[str, Any]] = MISSING,
    ) -> None:
        """
        Initializes a Command instance with the given parameters.

        Parameters
        ----------
        mode: :class:`Mode`
            Command mode to be used.
        pid: Union[:class:`int`, :class:`str`]
            Command PID (Parameter Identifier) to be used.
        n_bytes: :class:`int`
            The number of bytes expected in the response.
        name: :class:`str`
            The name of the command.
        description: :class:`str`
            A description of the command.
        min_values: Optional[Union[:class:`int`, :class:`float`, List[Union[:class:`int`, :class:`float`]]]]
            The minimum valid values for the command's parameters.
        max_values: Optional[Union[:class:`int`, :class:`float`, List[Union[:class:`int`, :class:`float`]]]]
            The maximum valid values for the command's parameters.
        units: Optional[Union[:class:`str`, List[:class:`str`]]]
            The units for the command's response.
        formula: Optional[:class:`Callable`]
            A formula for transforming the response value.
        command_args: Optional[Dict[:class:`str`, Any]]
            A dictionary containing the argument names and their expected types for formatting the command.
        """
        self.mode = mode
        self.pid = pid
        self.n_bytes = n_bytes
        self.name = name
        self.description = description
        self.min_values = min_values
        self.max_values = max_values
        self.units = units
        self.formula = formula

        self.command_args = command_args or {}
        self.is_formatted = False

    def _validate_placeholders(self) -> None:
        placeholders = set(findall(r"{(\w+)}", str(self.pid)))
        expected_placeholders = set(self.command_args.keys())

        if placeholders != expected_placeholders:
            missing = expected_placeholders - placeholders
            extra = placeholders - expected_placeholders
            raise ValueError(
                f"PID format mismatch. Missing placeholders: {missing}. Extra placeholders: {extra}."
            )

    def _format_arg(self, arg_name: str, arg_type: type, value: Union[str, int]) -> str:
        if not isinstance(value, arg_type):
            raise TypeError(
                f"Expected argument '{arg_name}' of type {arg_type.__name__}, got {type(value).__name__}."
            )

        expected_len = len(arg_name)

        if isinstance(value, int):
            if value < 0:
                raise ValueError(f"Argument '{arg_name}' cannot be negative.")
            formatted = f"{value:0{expected_len}X}"
        elif isinstance(value, str):
            formatted = value
        else:
            raise TypeError(
                f"Argument '{arg_name}' must be of type int or str, got {type(value).__name__}."
            )

        if len(formatted) != expected_len:
            raise ValueError(
                f"Argument '{arg_name}' must be {expected_len} characters long after formatting, got {len(formatted)}."
            )

        return formatted

    def __call__(self, *args: Any, checks: bool = True) -> Command:
        """
        Formats the command with the provided positional arguments and checks for validity.

        Parameters
        ----------
        *args: :class:`Any`
            The values for the arguments of the command, in the order they are defined in `command_args`.
        checks: :class:`bool`
            If `True`, performs validation checks on the arguments. Defaults to `True`.

        Returns
        -------
        :class:`Command`
            A new `Command` object with the formatted PID.

        Raises
        ------
        ValueError
            If the number of arguments does not match the expected number or if the placeholders are mismatched.
        TypeError
            If the argument type does not match the expected type.
        """
        if not self.command_args:
            raise ValueError(
                f"Command '{self}' should not be parametrized, as no arguments have been described."
            )

        if len(args) != len(self.command_args):
            raise ValueError(
                f"Expected {len(self.command_args)} arguments, got {len(args)}."
            )

        self._validate_placeholders()

        combined_args = {
            arg_name: (self._format_arg(arg_name, arg_type, value) if checks else value)
            for (arg_name, arg_type), value in zip(self.command_args.items(), args)
        }

        fmt_command = deepcopy(self)
        fmt_command.is_formatted = True
        fmt_command.pid = str(self.pid).format(**combined_args)

        return fmt_command

    def __repr__(self) -> str:
        return f"<Command {self.mode} {self.pid if isinstance(self.pid, str) else f'{self.pid:02X}'} {self.name or 'Unnamed'} [{', '.join(self.command_args.keys())}]>"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Command):
            return False

        return vars(self) == vars(value)

    def __hash__(self) -> int:
        return hash((self.mode, self.pid, self.name))

    def _return_digit(self, early_return: bool) -> str:
        """Return hex digit for expected response lines (early-return ELM327 DSL, page 34)."""
        if not (early_return and self.n_bytes and self.mode != Mode.AT):
            return ''

        data_bytes = 7
        n_lines = (self.n_bytes + (data_bytes - 1)) // data_bytes

        return f" {n_lines:X}" if 0 < n_lines < 16 else ''

    def _format_to_hex(self, value: Union[int, str]) -> str:
        return f"{value:02X}" if isinstance(value, int) else str(value)

    def build(self, early_return: bool = False) -> bytes:
        """
        Builds the query to be sent to the ELM327 device as a byte string.
        (The ELM327 is case-insensitive, ignores spaces and all control characters.)

        Parameters
        ----------
        early_return: :class:`bool`
            If set to `True`, appends a hex digit representing the expected number of responses in the query.
            Defaults to `False`.

        Returns
        -------
        :class:`bytes`
            The formatted query as a byte string, ready to be sent to the ELM327 device.

        Raises
        ------
        ValueError
            If arguments have not been set or are incorrectly formatted.
        """
        if self.command_args and not self.is_formatted:
            raise ValueError(
                f"Command has unset arguments for '{self.pid}': {self.command_args}"
            )

        mode = self._format_to_hex(self.mode.value)
        pid = self._format_to_hex(self.pid)
        return_digit = self._return_digit(early_return)

        query = f"{mode} {pid}{return_digit}\r"

        return query.encode()
