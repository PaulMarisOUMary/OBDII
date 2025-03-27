__title__ = "obdii"
__author__ = "PaulMarisOUMary"
__license__ = "MIT"
__copyright__ = "Copyright 2025-present PaulMarisOUMary"
__version__ = "0.3.1a0"

from logging import NullHandler, getLogger

from .basetypes import Context, Command, Mode, Protocol, Response
from .connection import Connection
from .commands import Commands
from .modes import at_commands

from .protocols import *


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