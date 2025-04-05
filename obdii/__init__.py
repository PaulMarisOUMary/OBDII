from importlib.metadata import version, PackageNotFoundError
from logging import NullHandler, getLogger
from pkgutil import extend_path

from .basetypes import Context, Command, Mode, Protocol, Response
from .connection import Connection
from .commands import Commands
from .modes import at_commands
from .protocols import *


__title__ = "obdii"
__author__ = "PaulMarisOUMary"
__license__ = "MIT"
__copyright__ = "Copyright 2025-present PaulMarisOUMary"

try:
    __version__ = version("py-obdii")
except PackageNotFoundError:
    __version__ = "0.0.0"
__path__ = extend_path(__path__, __name__)


commands = Commands()

__all__ = [
    "at_commands",
    "commands",
    "Connection",
    "Context",
    "Command",
    "Mode",
    "Protocol",
    "Response",
]

getLogger(__name__).addHandler(NullHandler())