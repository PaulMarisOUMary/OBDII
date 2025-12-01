"""
Unit tests for obdii.connection module.
"""
import pytest

from typing import List, Tuple

from obdii.command import Command
from obdii.connection import Connection
from obdii.mode import Mode
from obdii.modes.mode_at import ModeAT
from obdii.protocol import Protocol
from obdii.protocols.protocol_base import ProtocolBase
from obdii.response import Context, Response
from obdii.transports.transport_base import TransportBase
from obdii.transports import TransportPort, TransportWifi


class FakeTransport(TransportBase):
    def __init__(self) -> None:
        self.connected = False
        self.writes: List[bytes] = []
        self.read_buffer: bytes = b''
        self.closed = False

    def connect(self, **kwargs) -> None:
        self.connected = True

    def close(self) -> None:
        self.connected = False
        self.closed = True

    def write_bytes(self, query: bytes) -> None:
        if not self.connected:
            raise RuntimeError("not connected")
        self.writes.append(query)

    def read_bytes(self) -> bytes:
        if not self.connected:
            raise RuntimeError("not connected")
        return self.read_buffer

    def is_connected(self) -> bool:
        return self.connected


class TestTransportResolution:
    """Tests for transport resolution in Connection."""
    @pytest.mark.parametrize(
        ("transport_arg", "expected_type"),
        [
            ("COM5", TransportPort),
            (("127.0.0.1", 35000), TransportWifi),
        ],
        ids=["port-string->TransportPort", "tuple->TransportWifi"],
    )
    def test_resolve_transport_port_and_wifi(self, transport_arg, expected_type):
        conn = Connection(transport_arg, auto_connect=False)

        assert isinstance(conn.transport, expected_type)


    def test_resolve_transport_instance(self):
        ft = FakeTransport()

        conn = Connection(ft, auto_connect=False)

        assert conn.transport is ft


    def test_resolve_transport_invalid_type(self):
        bad = object()

        with pytest.raises(TypeError):
            _ = Connection(bad, auto_connect=False)  # type: ignore[arg-type]


class TestConnectLifecycle:
    """Connection.connect lifecycle (success and failure paths)."""
    def test_connect_success_calls_initialize_and_sets_flag(self, mocker):
        ft = FakeTransport()
        conn = Connection(ft, auto_connect=False)

        init_mock = mocker.patch.object(conn, "_initialize_connection")

        conn.connect()

        init_mock.assert_called_once()
        assert conn.init_completed is True
        assert ft.connected is True

    def test_connect_failure_closes_transport_and_raises(self, mocker):
        ft = FakeTransport()
        conn = Connection(ft, auto_connect=False)

        mocker.patch.object(ft, "connect", side_effect=Exception("boom"))

        with pytest.raises(ConnectionError):
            conn.connect()

        assert ft.closed is True
        assert conn.init_completed is False


class TestConnectionHelpers:
    """Helpers and proxies exposed by Connection (e.g., is_connected)."""
    def test_is_connected_proxies_transport(self):
        ft = FakeTransport()
        conn = Connection(ft, auto_connect=False)

        assert conn.is_connected() is False
        ft.connected = True
        assert conn.is_connected() is True


class TestQueryBehavior:
    """Query sending semantics including smart_query repeat behavior."""
    def test_query_builds_and_writes_and_waits(self, mocker):
        ft = FakeTransport()
        conn = Connection(ft, auto_connect=False, smart_query=False, early_return=False)
        ft.connected = True

        dummy_resp = Response(Context(Command(Mode.AT, 'I', 0), Protocol.AUTO), b"OK\r>", [b"OK", b'>'])
        wait_mock = mocker.patch.object(conn, "wait_for_response", return_value=dummy_resp)

        cmd = Command(Mode.AT, 'Z', 0)

        resp = conn.query(cmd)

        assert resp is dummy_resp
        assert ft.writes == [cmd.build(False)]
        wait_mock.assert_called_once()

    def test_query_uses_repeat_when_smart_query_enabled(self, mocker):
        ft = FakeTransport()
        conn = Connection(ft, auto_connect=False, smart_query=True)
        ft.connected = True

        dummy_resp = Response(Context(Command(Mode.AT, 'I', 0), Protocol.AUTO), b"OK\r>", [b"OK", b'>'])
        mocker.patch.object(conn, "wait_for_response", return_value=dummy_resp)

        cmd = Command(Mode.AT, 'I', 0)

        _ = conn.query(cmd)
        # second identical call should send REPEAT
        _ = conn.query(cmd)

        expected_first = cmd.build(False)
        expected_second = ModeAT.REPEAT.build()
        assert ft.writes == [expected_first, expected_second]


class TestWaitForResponse:
    """Waiting for raw bytes and parsing to Response, including fallback."""
    def test_wait_for_response_returns_parsed(self):
        ft = FakeTransport()
        ft.connected = True
        ft.read_buffer = b"LINE1\rLINE2\r>"
        conn = Connection(ft, auto_connect=False)

        class DummyHandler(ProtocolBase):
            def parse_response(self, rb):
                return Response(rb.context, rb.raw, rb.messages, parsed_data=[(b'X',)])

        conn.protocol_handler = DummyHandler()
        ctx = Context(Command(Mode.AT, 'I', 0), Protocol.AUTO)

        resp = conn.wait_for_response(ctx)

        assert isinstance(resp, Response)
        assert resp.raw == b"LINE1\rLINE2\r>"
        assert resp.parsed_data == [(b'X',)]

    def test_wait_for_response_unsupported_returns_fallback(self):
        ft = FakeTransport()
        ft.connected = True
        ft.read_buffer = b"DATA\r>"
        conn = Connection(ft, auto_connect=False)
        conn.init_completed = True

        class DummyHandler(ProtocolBase):
            def parse_response(self, rb):
                raise NotImplementedError()

        conn.protocol_handler = DummyHandler()
        ctx = Context(Command(Mode.AT, 'I', 0), Protocol.AUTO)

        resp = conn.wait_for_response(ctx)

        assert isinstance(resp, Response)
        assert resp.raw == b"DATA\r>"
        assert [m for m in resp.messages if m]  # non-empty messages list


class TestCloseAndContextManager:
    """close() behavior and context manager enter/exit semantics."""
    def test_close_calls_transport_close(self):
        ft = FakeTransport()
        conn = Connection(ft, auto_connect=False)
        ft.connected = True

        conn.close()

        assert ft.closed is True

    def test_context_manager_closes_on_exit(self):
        ft = FakeTransport()
        with Connection(ft, auto_connect=False) as conn:
            assert conn.is_connected() is False
            ft.connected = True
        assert ft.closed is True


class TestProtocolHelpers:
    """Protocol parsing/setting helpers and auto selection priority."""
    def test_parse_protocol_number_various(self):
        ft = FakeTransport()
        conn = Connection(ft, auto_connect=False)

        assert conn._parse_protocol_number("PROTO 0") == 0
        assert conn._parse_protocol_number("PROTO A") == 0xA
        assert conn._parse_protocol_number("proto c") == 0xC
        assert conn._parse_protocol_number("no number here!") == -1

    def test_set_protocol_to_sends_commands_and_parses(self, mocker):
        ft = FakeTransport()
        conn = Connection(ft, auto_connect=False)

        sent: List[Command] = []

        class DummyResp:
            def __init__(self, raw: bytes) -> None:
                self.raw = raw

        def fake_query(cmd: Command):
            sent.append(cmd)
            # Return a raw line that ends with hex digit '9'
            return DummyResp(b"PROTO 9\r>")

        mocker.patch.object(conn, "query", side_effect=fake_query)

        number = conn._set_protocol_to(Protocol.SAE_J1850_PWM)

        assert [c.name for c in sent] == ["SET_PROTOCOL", "DESC_PROTOCOL_N"]
        assert number == 9

    def test_get_supported_protocols_filters_and_defaults(self, mocker):
        ft = FakeTransport()
        conn = Connection(ft, auto_connect=False)

        def fake_set(proto: Protocol) -> int:
            # Support only two specific protocols
            return proto.value if proto in (Protocol.SAE_J1850_VPW, Protocol.ISO_15765_4_CAN) else -1

        mocker.patch.object(conn, "_set_protocol_to", side_effect=fake_set)

        supported = conn._get_supported_protocols()

        assert supported == [Protocol.SAE_J1850_VPW, Protocol.ISO_15765_4_CAN]

        # Now simulate none supported -> UNKNOWN
        mocker.patch.object(conn, "_set_protocol_to", return_value=-1)
        assert conn._get_supported_protocols() == [Protocol.UNKNOWN]

    def test_auto_protocol_chooses_preferred(self, mocker):
        ft = FakeTransport()
        conn = Connection(ft, auto_connect=False)

        # First call to _set_protocol_to (with initial protocol) returns AUTO
        # so that unwanted protocol path is taken.
        set_calls: List[Tuple[Protocol, int]] = []

        def fake_set(proto: Protocol) -> int:
            set_calls.append((proto, proto.value))
            # Report AUTO/UNKNOWN for first call to trigger supported search
            return proto.value

        mocker.patch.object(conn, "_set_protocol_to", side_effect=fake_set)

        # Provide supported protocols in mixed order; connection should pick the highest priority
        mocker.patch.object(conn, "_get_supported_protocols", return_value=[
            Protocol.SAE_J1850_VPW,
            Protocol.ISO_15765_4_CAN_D,
            Protocol.ISO_14230_4_KWP,
        ])

        class DummyProto(ProtocolBase):
            def parse_response(self, response_base):
                raise NotImplementedError()

        mocker.patch.object(ProtocolBase, "get_handler", return_value=DummyProto())

        conn._auto_protocol(Protocol.AUTO)

        # chosen protocol should be the first matching priority from preferences (CAN 0x09 over J1850/ISO)
        assert conn.protocol == Protocol.ISO_15765_4_CAN_D
        assert isinstance(conn.protocol_handler, ProtocolBase)
