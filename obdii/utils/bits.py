from re import escape, sub
from typing import Tuple


def split_hex_bytes(data: bytes) -> Tuple[bytes, ...]:
    """Split a bytes object of hexadecimal characters into 2-character chunks, where each chunk represents one byte (8 bits)."""
    if len(data) % 2 != 0:
        data = b'0' + data

    return tuple(data[i : i + 2] for i in range(0, len(data), 2))


def is_bytes_hex(data: bytes) -> bool:
    """Check if a bytes object contains only hexadecimal characters."""
    if not data:
        return False
    hex_chars = set(b'0123456789ABCDEFabcdef')
    return all(b in hex_chars for b in data)


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
