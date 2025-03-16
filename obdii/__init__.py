__title__ = "obdii"
__author__ = "PaulMarisOUMary"
__license__ = "MIT"
__copyright__ = "Copyright 2025-present PaulMarisOUMary"
__version__ = "0.1.0a5"

from logging import NullHandler, getLogger

from .connection import Connection
from .commands import commands
from .modes.modeat import at_commands

# We must __init__ .protocols to BaseProtocol.register supported protocols
from .protocols import *

__all__ = [
    "Connection",
    "commands",
    "at_commands",
]

getLogger(__name__).addHandler(NullHandler())