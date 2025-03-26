from logging import Handler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL, StreamHandler, getLogger
from os import environ
from re import escape, fullmatch, sub
from sys import platform
from typing import Any, Optional, Tuple

from .basetypes import BaseResponse


def split_by_byte(raw: bytes) -> Tuple[bytes, ...]:
    if len(raw) % 2 != 0:
        raw = b'0' + raw

    return tuple(raw[i:i+2] for i in range(0, len(raw), 2))


def is_bytes_hexadecimal(raw: bytes) -> bool:
    return bool(fullmatch(b"[0-9A-Fa-f]+", raw))


def filter_bytes(raw: bytes, *filter_bytes: bytes) -> bytes:
    pattern = b'|'.join(escape(filter_byte) for filter_byte in filter_bytes)

    return sub(pattern, b'', raw)


def bytes_to_string(raw: bytes) -> str:
    return raw.decode(errors="ignore").strip()


def debug_baseresponse(base_response: BaseResponse) -> str:
    return '\n'.join(f"[{bytes_to_string(line)}]" for line in base_response.messages[:-1]) + '\n'


def setup_logging(
    handler: Optional[Handler] = None,
    formatter: Optional[Formatter] = None,
    level: Optional[int] = None,
    root: bool = True,
) -> None:
    """A helper function to setup logging."""
    if not level:
        level = INFO

    if not handler:
        handler = StreamHandler()

    if not formatter:
        if isinstance(handler, StreamHandler) and _stream_supports_colour(handler.stream):
            formatter = _ColorFormatter()
        else:
            dt_fmt = "%Y-%m-%d %H:%M:%S"
            formatter = Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style='{')

    if root:
        logger = getLogger()
    else:
        library, _, _ = __name__.partition('.')
        logger = getLogger(library)

    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)

def _stream_supports_colour(stream: Any) -> bool:
    is_a_tty = hasattr(stream, "isatty") and stream.isatty()

    if "PYCHARM_HOSTED" in environ or environ.get("TERM_PROGRAM") == "vscode":
        return is_a_tty

    if platform != "win32":
        return is_a_tty

    return is_a_tty and "WT_SESSION" in environ

class _ColorFormatter(Formatter):
    LEVEL_COLORS = [
        (DEBUG, "\x1b[40;1m"),
        (INFO, "\x1b[34;1m"),
        (WARNING, "\x1b[33;1m"),
        (ERROR, "\x1b[31m"),
        (CRITICAL, "\x1b[41m"),
    ]

    FORMATS = {
        level: Formatter(
            f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        for level, colour in LEVEL_COLORS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[DEBUG]

        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)

        record.exc_text = None
        return output
