from typing import Dict, Iterable, List

from ..basetypes import BytesRows


class SupportedPIDS:
    def __init__(self, base_pid: int) -> None:
        self.base_pid = base_pid

    def __call__(self, parsed_data: BytesRows) -> List[int]:
        concatenated_data = sum(parsed_data, ())

        binary_string = ''.join(
            [f"{int(hex_value, 16):08b}" for hex_value in concatenated_data]
        )

        supported_pids = [
            self.base_pid + i for i, bit in enumerate(binary_string) if bit == "1"
        ]

        return supported_pids


class EnumeratedPIDS:
    def __init__(self, mapping: Dict) -> None:
        self.mapping = self._extend_mapping(mapping)

    def _extend_mapping(self, mapping: Dict) -> Dict:
        extended = {}

        for key, value in mapping.items():
            if isinstance(key, Iterable) and not isinstance(key, (bytes, int, str)):
                for k in key:
                    extended[k] = value
            else:
                extended[key] = value

        return extended

    def __call__(self, parsed_data: BytesRows) -> List:
        concatenated_data = sum(parsed_data, ())

        mapped_values = []

        for data in concatenated_data:
            hbtd = int(data, 16)
            mapped_values.append((hbtd, self.mapping.get(hbtd, None)))

        return mapped_values
