from __future__ import annotations

from enum import Enum
from typing import List, Any


_CATEGORY_BITS = {
    0b00: 'P',
    0b01: 'C',
    0b10: 'B',
    0b11: 'U',
}


class UnknownEnum(Enum):
    @classmethod
    def _missing_(cls, value: Any):
        for member in cls:
            if isinstance(member.value, tuple) and value in member.value:
                return member

        unknown = getattr(cls, "UNKNOWN", None)
        if unknown is not None:
            return unknown


class Category(UnknownEnum):
    UNKNOWN = None
    BODY = 'B'
    CHASSIS = 'C'
    POWERTRAIN = 'P'
    NETWORK = 'U'


class Scope(UnknownEnum):
    UNKNOWN = None
    GENERIC = '0'
    MANUFACTURER_SPECIFIC = '1'
    GENERIC_AND_MANUFACTURER = '2'
    GENERIC_AND_MANUFACTURER_MIXED = '3'


class System(UnknownEnum):
    UNKNOWN = None
    FUEL_AIR_METERING_AUX = '0'
    FUEL_AIR_METERING = '1'
    FUEL_AIR_METERING_INJECTOR = '2'
    IGNITION_OR_MISFIRE = '3'
    AUXILIARY_EMISSION_CONTROL = '4'
    SPEED_IDLE_CONTROL = '5'
    COMPUTER_OUTPUT_CIRCUITS = '6'
    TRANSMISSION = ('7', '8', '9')
    HYBRID_PROPULSION = ('A', 'B', 'C')


class DTC:
    """
    Diagnostic Trouble Code (DTC) representation.

    5 characters structured as follows:

    .. code-block:: none

        U    0    1    5    8
        |    |    |    |____|
        |    |    |    descriptor
        |    |    system
        |    scope
        category
    """

    __slots__ = ("code", "category", "scope", "system", "descriptor")

    code: str
    """Full DTC code, e.g. "U0158"."""
    category: Category
    """DTC category, e.g. `Category.NETWORK`."""
    scope: Scope
    """DTC scope, e.g. `Scope.GENERIC`."""
    system: System
    """DTC system, e.g. `System.FUEL_AIR_METERING`."""
    descriptor: str
    """DTC descriptor, e.g. "58"."""

    def __init__(self, raw: str) -> None:
        """
        Initialize DTC object.

        Parameters
        ----------
        *raw: str
            The raw DTC code string, e.g. "U0158".
        """
        raw = raw.strip().upper()

        if len(raw) != 5:
            raise ValueError(f"Invalid DTC code: {raw!r}.")

        self.code = raw
        self.category = Category(raw[0])
        self.scope = Scope(raw[1])
        self.system = System(raw[2])
        self.descriptor = raw[3:5]

    def __str__(self) -> str:
        return self.code

    def __repr__(self) -> str:
        return f"<DTC {self}>"

    @classmethod
    def from_bytes(cls, high: int, low: int) -> DTC:
        """
        Parse two raw bytes into a DTC.

        .. code-block:: none

            0xC1, 0x58
            1100 0001 0101 1000
            U 0  1    5    8
        """
        category = _CATEGORY_BITS[(high >> 6) & 0x03]
        number = ((high & 0x3F) << 8) | low
        return cls(f"{category}{number:04X}")

    @staticmethod
    def parse(unparsed: List[int]) -> List[DTC]:
        """
        Parse a raw Mode 03 CAN payload into a list of DTCs.

        .. code-block:: none

            [0x02, 0xC1, 0x58, 0x01, 0x96, 0x00, 0x00, 0x00]
                |   |_____|     |_____|     |___________|
            count    DTC #1      DTC #2      padding (ignored)

        Parameters
        ----------
        unparsed: List[int]
            The data to evaluate the formula against.
        """
        data_len = len(unparsed)
        if not data_len:
            return []

        count = unparsed[0]
        if count == 0:
            return []

        expected_len = 1 + count * 2
        if data_len < expected_len:
            raise ValueError(
                f"Payload too short, expected at least {expected_len} bytes for {count} DTCs, got {data_len}."
            )

        dtcs = []
        for i in range(count):
            offset = 1 + i * 2
            high, low = unparsed[offset], unparsed[offset + 1]
            dtcs.append(DTC.from_bytes(high, low))

        return dtcs
