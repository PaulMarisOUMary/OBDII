"""
Unit tests for obdii.command.Command class.
"""
import pytest

from obdii.basetypes import MISSING
from obdii.command import Command, Template
from obdii.mode import Mode


@pytest.fixture
def simple_command():
    """Fixture that returns a simple Command instance."""
    return Command(mode=Mode.REQUEST, pid=0x0C, expected_bytes=2, units="rpm")


@pytest.fixture
def template_command():
    """Fixture that returns a Command instance with a Template PID."""
    return Command(mode=Mode.AT, pid=Template("SET {val:int}"), expected_bytes=0)


class TestCommandInitialization:
    """Test Command initialization and attribute assignment."""

    def test_init_defaults(self):
        cmd = Command(mode=Mode.REQUEST, pid=0x01)
        assert cmd.mode == Mode.REQUEST
        assert cmd.pid == 0x01
        assert cmd.expected_bytes == 0
        assert cmd.name == "Unnamed"
        assert cmd.min_values is MISSING
        assert cmd.max_values is MISSING
        assert cmd.units is MISSING
        assert cmd.resolver is MISSING

    def test_init_full(self):
        def resolver(x): return x

        cmd = Command(
            mode=Mode.REQUEST,
            pid=0x0C,
            expected_bytes=2,
            min_values=0,
            max_values=16383.75,
            units="rpm",
            resolver=resolver
        )
        assert cmd.mode == Mode.REQUEST
        assert cmd.pid == 0x0C
        assert cmd.expected_bytes == 2
        assert cmd.min_values == 0
        assert cmd.max_values == 16383.75
        assert cmd.units == "rpm"
        assert cmd.resolver is resolver



class TestCommandEquality:
    """Test Command equality and hashing."""

    def test_equality_same_attributes(self, simple_command):
        other = Command(mode=Mode.REQUEST, pid=0x0C, expected_bytes=2, units="rpm")
        assert simple_command == other

    def test_equality_different_attributes(self, simple_command):
        other = Command(mode=Mode.REQUEST, pid=0x0D, expected_bytes=1, units="km/h")
        assert simple_command != other

    def test_equality_different_type(self, simple_command):
        assert simple_command != "Not a Command"

    def test_hash_consistency(self, simple_command):
        other = Command(mode=Mode.REQUEST, pid=0x0C, expected_bytes=2, units="rpm")
        assert hash(simple_command) == hash(other)

    def test_hash_difference(self, simple_command):
        other = Command(mode=Mode.REQUEST, pid=0x0D)
        assert hash(simple_command) != hash(other)


class TestCommandFormatting:
    """Test Command formatting via __call__."""

    def test_call_formats_template_pid(self, template_command):
        formatted_cmd = template_command(val=42)
        assert isinstance(formatted_cmd, Command)
        assert formatted_cmd.pid == "SET 42"
        assert formatted_cmd.mode == template_command.mode
        assert formatted_cmd.expected_bytes == template_command.expected_bytes

    def test_call_returns_new_instance(self, template_command):
        formatted_cmd = template_command(val=42)
        assert formatted_cmd is not template_command
        assert template_command.pid.template == "SET {val:int}"  # Original unchanged

    def test_call_non_template_pid_raises_typeerror(self, simple_command):
        with pytest.raises(TypeError, match="Cannot format command with non-template PID"):
            simple_command(val=42)

    def test_call_preserves_other_attributes(self):
        cmd = Command(mode=Mode.AT, pid=Template("{x}"), units='V', expected_bytes=1)
        formatted = cmd(x="TEST")
        assert formatted.units == 'V'
        assert formatted.expected_bytes == 1


class TestCommandBuild:
    """Test Command.build() method."""

    @pytest.mark.parametrize(
        ("mode", "pid", "expected_bytes"),
        [
            (Mode.REQUEST, 0x0C, b"01 0C\r"),
            (Mode.REQUEST, "0C", b"01 0C\r"),
            (Mode.AT, 'Z', b"AT Z\r"),
            (1, 12, b"01 0C\r"),  # Int mode/pid formatted to hex
        ],
        ids=["mode_request_hex", "mode_request_str", "mode_at", "int_values"]
    )
    def test_build_basic(self, mode, pid, expected_bytes):
        cmd = Command(mode=mode, pid=pid)
        assert cmd.build() == expected_bytes

    def test_build_with_template_raises_valueerror(self, template_command):
        with pytest.raises(ValueError, match="Cannot build command with unformatted PID template"):
            template_command.build()

    def test_build_formatted_template(self, template_command):
        formatted = template_command(val=10)
        assert formatted.build() == b"AT SET 10\r"

    @pytest.mark.parametrize(
        ("expected_bytes_val", "early_return", "expected_suffix"),
        [
            (None, True, b''),
            (0, True, b''),
            (3, False, b''),
            (3, True, b" 1"),
            (7, True, b" 1"),
            (8, True, b" 2"),
            (100, True, b" F"),
            (255, True, b''),
        ],
        ids=["none_bytes", "zero_bytes", "false_flag", "3_bytes", "7_bytes", "8_bytes", "max_byte", "large_bytes"]
    )
    def test_build_early_return(self, expected_bytes_val, early_return, expected_suffix):
        # Note: early_return logic in Command:
        # if not (early_return and self.expected_bytes and isinstance(self.expected_bytes, int) and self.mode != Mode.AT): return ''
        # n_lines = (self.expected_bytes + 6) // 7
        # return f" {n_lines:X}" if 0 < n_lines < 16 else ''
        
        cmd = Command(mode=Mode.REQUEST, pid=0x01, expected_bytes=expected_bytes_val)
        result = cmd.build(early_return=early_return)
        
        expected = b"01 01" + expected_suffix + b'\r'
        assert result == expected

    def test_build_early_return_at_mode_ignored(self):
        cmd = Command(mode=Mode.AT, pid='Z', expected_bytes=10)
        # AT commands shouldn't have return digit
        assert cmd.build(early_return=True) == b"AT Z\r"