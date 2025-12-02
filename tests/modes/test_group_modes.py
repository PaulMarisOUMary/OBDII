"""
Unit tests for obdii.modes.group_modes.GroupModes class.
"""
import pytest

from obdii.command import Command
from obdii.mode import Mode
from obdii.modes.group_commands import GroupCommands
from obdii.modes.group_modes import GroupModes
from obdii.modes import Mode01, Mode02, Mode03, Mode04, Mode09


@pytest.fixture
def group_modes():
    """Fixture that returns an instance of GroupModes."""
    return GroupModes()


class TestGroupModesInitialization:
    """Test GroupModes initialization."""

    def test_modes_registry_is_loaded(self, group_modes):
        assert group_modes.modes is not None
        assert len(group_modes.modes) > 0
        assert Mode.REQUEST in group_modes.modes
        assert Mode.VEHICLE_INFO in group_modes.modes


class TestGroupModesAccess:
    """Test accessing modes and commands via __getitem__."""

    @pytest.mark.parametrize(
        ("key", "expected_type"),
        [
            (0x01, Mode01),
            (0x02, Mode02),
            (0x03, Mode03),
            (0x04, Mode04),
            (0x09, Mode09),
        ],
        ids=["mode_01", "mode_02", "mode_03", "mode_04", "mode_09"]
    )
    def test_getitem_by_mode_id(self, group_modes, key, expected_type):
        mode = group_modes[key]
        assert isinstance(mode, expected_type)
        assert isinstance(mode, GroupCommands)

    @pytest.mark.parametrize(
        ("key", "expected_cmd_name"),
        [
            ("ENGINE_LOAD", "ENGINE_LOAD"),         # Mode 01
            ("DTC_ENGINE_LOAD", "DTC_ENGINE_LOAD"), # Mode 02
            ("GET_DTC", "GET_DTC"),                 # Mode 03
            ("CLEAR_DTC", "CLEAR_DTC"),             # Mode 04
            ("VIN", "VIN"),                         # Mode 09
        ],
        ids=["mode01_cmd", "mode02_cmd", "mode03_cmd", "mode04_cmd", "mode09_cmd"]
    )
    def test_getitem_by_command_name(self, group_modes, key, expected_cmd_name):
        cmd = group_modes[key]
        assert isinstance(cmd, Command)
        assert cmd.name == expected_cmd_name

    def test_getitem_invalid_mode_id_raises_keyerror(self, group_modes):
        with pytest.raises(KeyError):
            group_modes[99]

    def test_getitem_invalid_command_name_raises_keyerror(self, group_modes):
        with pytest.raises(KeyError):
            group_modes["UNKNOWN_CMD"]

    def test_getitem_invalid_type_raises_typeerror(self, group_modes):
        with pytest.raises(TypeError):
            group_modes[1.5]


class TestGroupModesIteration:
    """Test iteration over GroupModes."""

    def test_iter_yields_all_commands(self, group_modes):
        cmds = list(group_modes)
        names = [c.name for c in cmds]

        assert "ENGINE_LOAD" in names
        assert "DTC_ENGINE_LOAD" in names
        assert "GET_DTC" in names
        assert "CLEAR_DTC" in names
        assert "VIN" in names

    def test_len_returns_total_count(self, group_modes):
        total_len = len(group_modes)
        expected_len = sum(len(mode) for mode in group_modes.modes.values())

        assert total_len == expected_len
        assert total_len > 0


class TestGroupModesMembership:
    """Test __contains__ and has_command."""

    def test_contains_command_instance(self, group_modes):
        cmd = group_modes["ENGINE_LOAD"]
        assert cmd in group_modes

    def test_contains_command_name(self, group_modes):
        assert "ENGINE_LOAD" in group_modes
        assert "engine_load" in group_modes

    def test_does_not_contain_unknown_name(self, group_modes):
        assert "UNKNOWN" not in group_modes
