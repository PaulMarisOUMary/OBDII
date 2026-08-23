from importlib.metadata import PackageNotFoundError, version
from logging import NullHandler, getLogger
from pkgutil import extend_path

from .command import Command, Template
from .connection import Connection
from .mode import Mode
from .modes import at_commands, commands
from .protocol import Protocol
from .response import Context, Response, ResponseBase

__title__ = "obdii"
__author__ = "PaulMarisOUMary"
__license__ = "MIT"
__copyright__ = "Copyright 2025-present PaulMarisOUMary"

try:
    __version__ = version("py-obdii")
except PackageNotFoundError:
    __version__ = "0.0.0"
__path__ = extend_path(__path__, __name__)


__all__ = [
    "Command",
    "Connection",
    "Context",
    "Mode",
    "Protocol",
    "Response",
    "ResponseBase",
    "Template",
    "at_commands",
    "commands",
]

getLogger(__name__).addHandler(NullHandler())
