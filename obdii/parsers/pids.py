from typing import Any, Dict, Iterable, List, Tuple, Union

from ..basetypes import BytesRows


class SupportedPIDS:
    """
    Parse supported PIDs from the response data.

    Each bit in the 4 byte (32 bit) response represents support for one PID, starting from the Base PID.
    A bit set to 1 indicates the PID is supported, 0 means it is not.
    Bits are read from most-significant to least-significant.

    Example
    -------
    .. code-block:: python3

        parsed_data = [(b"BE", b"1F", b"A8", b"13")]
        # B    E    1    F    A    8    1    3
        # 1011 1110 0001 1111 1010 1000 0001 0011

        supported_pids = SupportedPIDS(0x01)
        result = supported_pids(parsed_data)

        >>> result
        [0x01, 0x03, 0x04, 0x05, 0x06, 0x07, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x13, 0x15, 0x1C, 0x1F, 0x20]
    """

    def __init__(self, base_pid: int) -> None:
        """
        Initialize SupportedPIDS with a given base PID.

        Parameters
        ----------
        base_pid: :class:`int`
            The base PID from which the support bits start.
        """
        self.base_pid = base_pid

    def __call__(self, parsed_data: BytesRows) -> List[int]:
        """
        Parse supported PIDs from the response data.

        Parameters
        ----------
        parsed_data: BytesRows
            The parsed response data containing hex byte strings.

        Returns
        -------
        List[:class:`int`]
            List of supported PIDs.
        """
        concatenated_data = sum(parsed_data, ())

        binary_string = ''.join(
            f"{int(hex_value, 16):08b}" for hex_value in concatenated_data
        )

        supported_pids = [
            self.base_pid + i for i, bit in enumerate(binary_string) if bit == '1'
        ]

        return supported_pids


class EnumeratedPIDS:
    """
    Map parsed data bytes to enumerated values.

    Example
    -------
    .. code-block:: python3

        parsed_data = [(b"00", b"00")]

        fuel_system_status = EnumeratedPIDS(
            {
                0: "The motor is off",
                1: "Open loop due to insufficient engine temperature",
                2: "Closed loop, using oxygen sensor feedback to determine fuel mix",
                4: "Open loop due to engine load OR fuel cut due to deceleration",
                8: "Open loop due to system failure",
                16: "Closed loop, using at least one oxygen sensor but there is a fault in the feedback system",
            }
        )
        result = fuel_system_status(parsed_data)

        >>> result
        [(0, "The motor is off"), (0, "The motor is off")]
    """

    def __init__(self, mapping: Dict[Union[int, Iterable[int]], Any]) -> None:
        """
        Initialize EnumeratedPIDS with a mapping dictionary.

        Parameters
        ----------
        mapping: Dict[Union[:class:`int`, Iterable[:class:`int`]], Any]
            A dictionary mapping byte values to their corresponding enumerated meanings.
        """
        self.mapping = self._extend_mapping(mapping)

    def _extend_mapping(
        self, mapping: Dict[Union[int, Iterable[int]], Any]
    ) -> Dict[int, Any]:
        extended = {}

        for key, value in mapping.items():
            if isinstance(key, Iterable) and not isinstance(key, (bytes, int, str)):
                for k in key:
                    extended[k] = value
            else:
                extended[key] = value

        return extended

    def __call__(self, parsed_data: BytesRows) -> List[Tuple[int, Any]]:
        """
        Map parsed data bytes to enumerated values.

        Parameters
        ----------
        parsed_data: BytesRows
            The parsed response data containing hex byte strings.

        Returns
        -------
        List[Tuple[int, Any]]
            List of tuples containing the byte value and its corresponding enumerated meaning.
        """
        concatenated_data = sum(parsed_data, ())

        mapped_values = []

        for data in concatenated_data:
            hbtd = int(data, 16)
            mapped_values.append((hbtd, self.mapping.get(hbtd, None)))

        return mapped_values
