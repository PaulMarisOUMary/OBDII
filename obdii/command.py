
from copy import deepcopy
from re import findall
from typing import Any, Callable, Dict, Optional, Union

from .basetypes import OneOrMany, Real
from .mode import Mode


class Command():
    def __init__(self, 
            mode: Mode,
            pid: Union[int, str],
            n_bytes: int,
            name: str,
            description: Optional[str] = None,
            min_values: Optional[OneOrMany[Real]] = None,
            max_values: Optional[OneOrMany[Real]] = None,
            units: Optional[OneOrMany[str]] = None,
            formula: Optional[Callable] = None,
            command_args: Optional[Dict[str, Any]] = None,
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
        description: Optional[:class:`str`]
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

    def __call__(self, *args: Any, checks: bool = True) -> "Command":
        """
        Formats the command with the provided arguments and checks for validity.

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
        expected_args = len(self.command_args)

        if not expected_args:
            raise ValueError(f"Command '{self.__repr__()}' should not be parametrized, as no arguments has been described")

        received_args = len(args)
        if expected_args != received_args:
            raise ValueError(f"{self.__repr__()} expects {expected_args} argument(s), but got {received_args}")

        actual_placeholders = set(findall(r"{(\w+)}", str(self.pid)))
        expected_placeholders = set(self.command_args.keys())

        if actual_placeholders != expected_placeholders:
            missing = expected_placeholders - actual_placeholders
            extra = actual_placeholders - expected_placeholders
            raise ValueError(f"PID format mismatch. Missing placeholders: {missing}. Extra placeholders: {extra}")
        
        fmt_command = deepcopy(self)
        combined_args = {}
        try:
            for (arg_name, arg_type), value in zip(self.command_args.items(), args):
                if checks:
                    if not isinstance(value, arg_type):
                        raise TypeError(f"Argument '{arg_name}' must be of type {arg_type}, but got {type(value).__name__}")

                    arg_len = len(arg_name)
                    if isinstance(value, int):
                        if value < 0:
                            raise ValueError(f"Argument '{arg_name}' cannot be negative (got {value}).")
                        formatted_value = f"{value:0{arg_len}X}"

                        if len(formatted_value) > arg_len:
                            raise ValueError(f"Formatted value '{formatted_value}' exceeds expected length {len(arg_name)} for argument '{arg_name}'")
                        value = formatted_value

                    elif isinstance(value, str) and len(value) != arg_len:
                        raise ValueError(f"Argument '{arg_name}' should have length {arg_len}, but got {len(value)}")

                combined_args[arg_name] = value

            fmt_command.is_formatted = True
            fmt_command.pid = str(self.pid).format(**combined_args)
        except Exception as e:
            raise e

        return fmt_command

    def __repr__(self) -> str:
        return f"<Command {self.mode} {self.pid if isinstance(self.pid, str) else f'{self.pid:02X}'} {self.name or 'Unnamed'} [{', '.join(self.command_args.keys())}]>"
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Command):
            return False

        return vars(self) == vars(value)
    
    def __hash__(self) -> int:
        return hash((self.mode, self.pid, self.name))

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
            raise ValueError(f"Command has unset arguments for '{self.pid}': {self.command_args}")

        mode = self.mode.value
        pid = self.pid

        return_digit = ''
        if early_return and self.n_bytes and self.mode != Mode.AT:
            data_bytes = 7
            n_lines = self.n_bytes // data_bytes + (1 if self.n_bytes % data_bytes != 0 else 0)
            if 0 < n_lines < 16:
                return_digit = f" {n_lines:X}"

        if isinstance(mode, int):
            mode = f"{mode:02X}"
        if isinstance(pid, int):
            pid = f"{pid:02X}"

        return f"{mode} {pid}{return_digit}\r".encode()