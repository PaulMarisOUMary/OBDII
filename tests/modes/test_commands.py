"""
Unit tests for obdii.modes.commands.
"""
import pytest

from obdii.modes import Mode01, Mode02, Mode03, Mode04, Mode09
from obdii.modes.group_modes import GroupModes


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
def test_commands_getitem_int(key, mode_cls, expected_exc):
    commands = GroupModes()

    if expected_exc:
        with pytest.raises(expected_exc):
            _ = commands[key]
        return

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
def test_commands_getitem_str(key, mode_cls, attr, expected_exc):
    commands = GroupModes()

    if expected_exc:
        with pytest.raises(expected_exc):
            _ = commands[key]
        return

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
def test_commands_getitem_int_int(mode_key, pid, mode_cls, attr, expected_exc):
    commands = GroupModes()

    if expected_exc:
        with pytest.raises(expected_exc):
            _ = commands[mode_key][pid]
        return

    expected = getattr(mode_cls(), attr)
    result = commands[mode_key][pid]
    assert result == expected