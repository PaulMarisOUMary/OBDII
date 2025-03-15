from functools import partial
from logging import Handler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL, StreamHandler, getLogger
from os import environ
from sys import platform
from typing import Any, List, Optional

from .basetypes import BaseResponse


def bytes_to_string(raw_response: List[bytes], filter_bytes: List[bytes] = []) -> str:
    filtered_response = [c for c in raw_response if c not in filter_bytes]
    return b''.join(filtered_response).decode(errors="ignore").strip()

filter_bts = partial(bytes_to_string, filter_bytes=[b'\r', b'>'])

def debug_baseresponse(base_response: BaseResponse) -> str:
    out = ''

    for line in base_response.message[:-1]: # omit prompt line
        out += f"[{filter_bts(line)}]\n"
    
    return out


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
