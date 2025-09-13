from importlib.metadata import version, PackageNotFoundError
from logging import NullHandler, getLogger
from pkgutil import extend_path

from .command import Command
from .connection import Connection
from .mode import Mode
from .modes import at_commands, commands
from .protocol import Protocol
from .response import ResponseBase, Context, Response

# note: Need to import protocols to register them
from . import protocols  # noqa: F401


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
    "at_commands",
    "commands",
    "Command",
    "Connection",
    "Context",
    "Mode",
    "Protocol",
    "Response",
    "ResponseBase",
]

getLogger(__name__).addHandler(NullHandler())
