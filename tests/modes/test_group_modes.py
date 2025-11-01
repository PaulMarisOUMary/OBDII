"""
Unit tests for obdii.modes.group_modes module.
"""
import pytest

from typing import Any

from obdii.command import Command
from obdii.mode import Mode
from obdii.modes import Mode01, Mode02, Mode03, Mode04, Mode09
from obdii.modes.group_commands import GroupCommands
from obdii.modes.group_modes import GroupModes


class FakeMode(GroupCommands):
    pass


def make_cmd(pid: int, name: str) -> Command:
    return Command(mode=Mode.REQUEST, pid=pid, n_bytes=2, name=name)


class TestGroupModesUnit:
    """Unit tests using mocked modes."""

    def test_iter_yields_commands_from_all_modes(self, mocker):
        mode1 = FakeMode()
        setattr(mode1, "RPM", make_cmd(0x0C, "RPM"))
        setattr(mode1, "SPEED", make_cmd(0x0D, "SPEED"))

        mode9 = FakeMode()
        setattr(mode9, "VIN", make_cmd(0x02, "VIN"))

        mocker.patch("obdii.modes.group_modes.MODE_REGISTRY", {0x01: mode1, 0x09: mode9})

        gm = GroupModes()
        names = {cmd.name for cmd in gm}
        assert names == {"RPM", "SPEED", "VIN"}

    def test_getitem_by_str_returns_command(self):
        gm = GroupModes()
        rpm = make_cmd(0x0C, "RPM")
        setattr(gm, "RPM", rpm)

        assert gm["rpm"] is rpm
        assert gm["RPM"] is rpm

    def test_getitem_by_str_missing_raises_keyerror(self):
        gm = GroupModes()
        with pytest.raises(KeyError, match="Command 'RPM' not found"):
            _ = gm["RPM"]

    def test_getitem_by_int_returns_mode(self, mocker):
        mode1 = FakeMode()
        setattr(mode1, "RPM", make_cmd(0x0C, "RPM"))
        mocker.patch("obdii.modes.group_modes.MODE_REGISTRY", {0x01: mode1})

        gm = GroupModes()
        mode = gm[0x01]
        assert isinstance(mode, GroupCommands)

    def test_getitem_by_int_missing_raises_keyerror(self, mocker):
        mocker.patch("obdii.modes.group_modes.MODE_REGISTRY", {})
        gm = GroupModes()
        with pytest.raises(KeyError, match="Mode '1' not found"):
            _ = gm[1]

    def test_getitem_invalid_type_raises_typeerror(self):
        gm = GroupModes()
        bad: Any = 1.23
        with pytest.raises(TypeError, match="Invalid key type"):
            _ = gm.__getitem__(bad)


class TestGroupModesIntegration:
    """Integration tests using real Mode instances."""

    @pytest.mark.parametrize(
        ("key", "mode_cls", "expected_exc"),
        [
            (1, Mode01, None),
            (2, Mode02, None),
            (3, Mode03, None),
            (4, Mode04, None),
            (9, Mode09, None),
            (0, None, KeyError),
        ],
        ids=["mode_01", "mode_02", "mode_03", "mode_04", "mode_09", "invalid_mode"],
    )
    def test_getitem_by_int(self, key, mode_cls, expected_exc):
        commands = GroupModes()

        if expected_exc:
            with pytest.raises(expected_exc):
                _ = commands[key]
        else:
            result = commands[key]
            assert result == mode_cls()

    @pytest.mark.parametrize(
        ("key", "mode_cls", "attr", "expected_exc"),
        [
            ("SUPPORTED_PIDS_A", Mode01, "SUPPORTED_PIDS_A", None),
            ("", None, None, KeyError),
        ],
        ids=["supported_pids_a", "empty_key"],
    )
    def test_getitem_by_str(self, key, mode_cls, attr, expected_exc):
        commands = GroupModes()

        if expected_exc:
            with pytest.raises(expected_exc):
                _ = commands[key]
        else:
            expected = getattr(mode_cls(), attr)
            result = commands[key]
            assert result == expected

    @pytest.mark.parametrize(
        ("mode_key", "pid", "mode_cls", "attr", "expected_exc"),
        [
            (1, 0, Mode01, "SUPPORTED_PIDS_A", None),
            (0, 0, None, None, KeyError),
        ],
        ids=["mode_01_supported_pids_a", "invalid_mode_then_pid"],
    )
    def test_getitem_chained(self, mode_key, pid, mode_cls, attr, expected_exc):
        commands = GroupModes()

        if expected_exc:
            with pytest.raises(expected_exc):
                _ = commands[mode_key][pid]
        else:
            expected = getattr(mode_cls(), attr)
            result = commands[mode_key][pid]
            assert result == expected
