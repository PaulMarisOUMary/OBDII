import pytest

from typing import Callable

from obdii import Context, Command, Protocol, ResponseBase, Response
from obdii.protocols.protocol_base import ProtocolBase


@pytest.fixture(scope="session")
def protocol_impl() -> Callable[[bytes, Command, Protocol, ProtocolBase], Response]:
    def parse_response(raw: bytes, command: Command, protocol: Protocol, handler: ProtocolBase) -> Response:
        ctx = Context(command, protocol)
        rb = ResponseBase(ctx, raw)

        return handler.parse_response(rb)
    return parse_response