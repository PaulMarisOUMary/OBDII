from typing import Any, Dict, List, Type

from serial.tools import list_ports

from ..basetypes import MISSING
from ..modes import at_commands
from ..transports.transport_base import TransportBase
from ..transports.transport_port import TransportPort
from ..transports.transport_wifi import TransportWifi


def scan_transports(
    candidates: List[Dict[str, Any]],
    transport_cls: Type[TransportBase],
    probe: bytes = MISSING,
    return_first: bool = False,
    **kwargs,
) -> List[TransportBase]:
    """
    Attempt to detect working transports from a list of candidates.

    Parameters
    ----------
    candidates : List[Dict[:class:`str`, Any]]
        List of transport configuration dictionaries. For example, for serial: [{"port": "COM3"}], for WiFi: [{"address": "192.168.0.10", "port": 35000}]
    transport_cls: Type[:class:`~obdii.transports.transport_base.TransportBase`]
        Transport class to instantiate for probing
        (e.g., :class:`~obdii.transports.transport_port.TransportPort`, :class:`~obdii.transports.transport_wifi.TransportWifi`).
    probe : :class:`bytes`
        Byte sequence to send to test the transport. Defaults to `at_commands.VERSION_ID.build()`.
    return_first : :class:`bool`
        If True, stop scanning and return after the first valid
        transport is found.

    **kwargs: :class:`dict`
        Additional keyword arguments forwarded to the transport's ``connect`` method.
    """
    results = []

    command_sequence = probe or at_commands.VERSION_ID.build()

    for candidate in candidates:
        transport = None
        try:
            transport = transport_cls(**candidate)

            transport.connect(**kwargs)
            transport.write_bytes(command_sequence)
            response = transport.read_bytes()

            if b"ELM327" in response or b'>' in response:
                results.append(transport)

                if return_first:
                    break
        except Exception:
            continue
        finally:
            if transport:
                transport.close()

    return results


def scan_ports(return_first: bool = True, **kwargs):
    """Scan available serial ports for ELM327 compatible devices."""
    candidates = [{"port": port.device} for port in list_ports.comports()]

    return scan_transports(
        candidates, TransportPort, return_first=return_first, **kwargs
    )


def scan_wifi(return_first: bool = True, **kwargs):
    """Scan common WiFi endpoints for ELM327 compatible devices."""
    common = [
        ("192.168.0.10", 35000),  # Most common
        ("192.168.1.10", 35000),  # Some clones
        ("192.168.0.74", 23),  # OBDKey WLAN
    ]

    candidates = [{"address": addr, "port": port} for addr, port in common]

    return scan_transports(
        candidates, TransportWifi, return_first=return_first, **kwargs
    )
