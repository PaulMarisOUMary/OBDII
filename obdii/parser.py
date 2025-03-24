from typing import List

from .basetypes import T_Parsed_Data


class SupportedPIDS():
    def __init__(self, base_pid: int) -> None:
        self.base_pid = base_pid
    
    def __call__(self, parsed_data: T_Parsed_Data) -> List[int]:
        concatenated_data = sum(parsed_data, ())

        binary_string = ''.join([f"{int(hex_value, 16):08b}" for hex_value in concatenated_data])

        supported_pids = [
            self.base_pid + i for i, bit in enumerate(binary_string) if bit == "1"
        ]

        return supported_pids


