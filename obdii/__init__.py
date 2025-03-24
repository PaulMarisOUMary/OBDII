__title__ = "obdii"
__author__ = "PaulMarisOUMary"
__license__ = "MIT"
__copyright__ = "Copyright 2025-present PaulMarisOUMary"
__version__ = "0.2.0a0"

from logging import NullHandler, getLogger

from .connection import Connection
from .commands import Commands
from .modes import at_commands
from .protocol import Protocol

from .protocols import *

# Initialize Commands
commands = Commands()

__all__ = [
    "at_commands",
    "commands",
    "Connection",
    "Protocol",
]

getLogger(__name__).addHandler(NullHandler())