"""
Unit tests for obdii.modes.group_commands module.
"""
import pytest

from obdii.command import Command
from obdii.mode import Mode
from obdii.modes.group_commands import GroupCommands


class DummyMode(GroupCommands):
    pass


def make_cmd(pid: int, name: str) -> Command:
    return Command(mode=Mode.REQUEST, pid=pid, n_bytes=2, name=name)


class TestGroupCommandsBasics:
    def test_len_counts_only_commands(self):
        mode = DummyMode()
        setattr(mode, "SPEED", make_cmd(0x0D, "SPEED"))
        setattr(mode, "RPM", make_cmd(0x0C, "RPM"))
        setattr(mode, "not_a_command", 123)

        assert len(mode) == 2
        assert "<Mode Commands: 2>" == repr(mode)

    def test_iter_yields_commands(self):
        mode = DummyMode()
        setattr(mode, "RPM", make_cmd(0x0C, "RPM"))
        setattr(mode, "SPEED", make_cmd(0x0D, "SPEED"))

        names = {cmd.name for cmd in mode}
        assert names == {"RPM", "SPEED"}

    @pytest.mark.parametrize(
        ("pid", "present"),
        [
            (0x0C, True),
            (0x0D, True),
            (0x05, False),
        ],
        ids=["rpm", "speed", "missing"],
    )
    def test_getitem_by_pid(self, pid, present):
        mode = DummyMode()
        setattr(mode, "RPM", make_cmd(0x0C, "RPM"))
        setattr(mode, "SPEED", make_cmd(0x0D, "SPEED"))

        if present:
            assert mode[pid].pid == pid
        else:
            with pytest.raises(KeyError, match=str(pid)):
                _ = mode[pid]

    @pytest.mark.parametrize(
        ("key",),
        [("0C",), ("RPM",), (None,), (1.23,)],
        ids=["str_hex", "str_name", "none", "float"],
    )
    def test_getitem_invalid_types_raise_keyerror(self, key):
        mode = DummyMode()
        setattr(mode, "RPM", make_cmd(0x0C, "RPM"))
        with pytest.raises(KeyError):
            _ = mode[key]

    def test_has_command_by_name_and_instance(self):
        mode = DummyMode()
        rpm = make_cmd(0x0C, "RPM")
        setattr(mode, "RPM", rpm)

        assert mode.has_command("rpm") is True
        assert mode.has_command("RPM") is True
        assert mode.has_command(rpm) is True
        assert mode.has_command("SPEED") is False

    def test_equality_semantics(self):
        a = DummyMode()
        b = DummyMode()
        setattr(a, "RPM", make_cmd(0x0C, "RPM"))
        setattr(b, "RPM", make_cmd(0x0C, "RPM"))

        assert a == b
        setattr(b, "SPEED", make_cmd(0x0D, "SPEED"))
        assert a != b
        assert (a == object()) is False
