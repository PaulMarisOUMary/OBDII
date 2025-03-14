from typing import Any, List

def bytes_to_string(raw_response: List[bytes], filter_bytes: List[bytes] = []) -> str:
    filtered_response = [c for c in raw_response if c not in filter_bytes]
    return b''.join(filtered_response).decode(errors="ignore")
