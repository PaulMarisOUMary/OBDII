"""
Unit tests for obdii.modes.group_commands.GroupCommands class.
"""
import pytest

from obdii.command import Command, Template
from obdii.modes.group_commands import GroupCommands


class MockCommands(GroupCommands):
    """Mock GroupCommands subclass for testing."""
    CMD1 = Command(mode=1, pid=0x01)
    CMD2 = Command(mode=1, pid=0x02)
    CMD3 = Command(mode=1, pid="03")
    CMD4 = Command(mode=1, pid=Template("04 {X:str}"))

    _PRIVATE = Command(mode=1, pid=0x05)

    OTHER = "Not a command"


@pytest.fixture
def group_commands():
    """Fixture that returns an instance of MockCommands."""
    return MockCommands()


class TestGroupCommandsInitialization:
    """Test GroupCommands initialization and attribute handling."""

    def test_command_names_are_set_automatically(self, group_commands):
        assert group_commands.CMD1.name == "CMD1"
        assert group_commands.CMD2.name == "CMD2"
        assert group_commands.CMD3.name == "CMD3"
        assert group_commands.CMD4.name == "CMD4"

    def test_private_attributes_are_named_but_ignored_in_iter(self, group_commands):
        assert group_commands._PRIVATE.name == "_PRIVATE"


class TestGroupCommandsAccess:
    """Test accessing commands via __getitem__."""

    @pytest.mark.parametrize(
        ("key", "expected_cmd_name"),
        [
            ("CMD1", "CMD1"),
            ("cmd1", "CMD1"),
            ("CMD2", "CMD2"),
            ("CMD3", "CMD3"),
            ("CMD4", "CMD4"),
        ],
        ids=["upper_case", "lower_case", "cmd2", "cmd3", "cmd4"]
    )
    def test_getitem_by_name(self, group_commands, key, expected_cmd_name):
        cmd = group_commands[key]
        assert isinstance(cmd, Command)
        assert cmd.name == expected_cmd_name

    @pytest.mark.parametrize(
        ("pid", "expected_cmd_name"),
        [
            (0x01, "CMD1"),
            (0x02, "CMD2"),
        ],
        ids=["pid_1", "pid_2"]
    )
    def test_getitem_by_pid(self, group_commands, pid, expected_cmd_name):
        cmd = group_commands[pid]
        assert isinstance(cmd, Command)
        assert cmd.name == expected_cmd_name

    def test_getitem_with_str_pid_raises_keyerror(self, group_commands):
        with pytest.raises(KeyError):
            group_commands["03"]

    def test_getitem_invalid_name_raises_keyerror(self, group_commands):
        with pytest.raises(KeyError):
            group_commands["UNKNOWN"]

    def test_getitem_non_command_attribute_raises_keyerror(self, group_commands):
        with pytest.raises(KeyError):
            group_commands["OTHER"]

    def test_getitem_invalid_pid_raises_keyerror(self, group_commands):
        with pytest.raises(KeyError):
            group_commands[99]

    def test_getitem_invalid_type_raises_typeerror(self, group_commands):
        with pytest.raises(TypeError):
            group_commands[1.5]


class TestGroupCommandsIteration:
    """Test iteration and length of GroupCommands."""

    def test_iter_yields_only_public_commands(self, group_commands):
        cmds = list(group_commands)
        names = [c.name for c in cmds]
        
        assert len(cmds) == 4
        assert "CMD1" in names
        assert "CMD2" in names
        assert "CMD3" in names
        assert "CMD4" in names

        assert "_PRIVATE" not in names

        assert "OTHER" not in names

    def test_len_returns_count_of_public_commands(self, group_commands):
        assert len(group_commands) == 4


class TestGroupCommandsMembership:
    """Test __contains__ and has_command."""

    def test_contains_command_instance(self, group_commands):
        assert group_commands.CMD1 in group_commands

    def test_contains_command_name_str(self, group_commands):
        assert "CMD1" in group_commands
        assert "cmd1" in group_commands

    def test_does_not_contain_unknown_command(self, group_commands):
        unknown_cmd = Command(mode=1, pid=0x99)
        assert unknown_cmd not in group_commands

    def test_does_not_contain_unknown_name(self, group_commands):
        assert "UNKNOWN" not in group_commands

    def test_does_not_contain_non_command_attribute(self, group_commands):
        assert "OTHER" not in group_commands