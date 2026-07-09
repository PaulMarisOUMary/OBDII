from re import escape, sub
from typing import List, Union


def filter_bytes(data: bytes, *patterns: bytes) -> bytes:
    """Remove all occurrences of specified byte patterns from a bytes object."""
    if not patterns:
        return data

    if len(patterns) == 1 and len(patterns[0]) == 1:
        return data.replace(patterns[0], b'')

    pattern = b'|'.join(escape(p) for p in patterns)
    return sub(pattern, b'', data)


def bytes_to_string(data: bytes) -> str:
    """Decode a bytes object to a string, ignoring errors and stripping whitespace."""
    if not data:
        return ''
    return data.decode(errors="ignore").strip()


def hex_to_ints(line: bytes) -> List[int]:
    """Convert a bytes of hexadecimal characters to a list of integers, where each integer represents one byte."""
    return list(bytes.fromhex(line.decode("ascii")))


def hex_byte_length(value: Union[int, str]) -> int:
    """Number of bytes needed to represent a value once hex-encoded."""
    if isinstance(value, int):
        return max(1, (value.bit_length() + 7) // 8)
    return (len(value) + 1) // 2
