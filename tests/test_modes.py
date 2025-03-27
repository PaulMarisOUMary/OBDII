import pytest

from obdii.basetypes import Command
from obdii.modes import ModeAT, Mode01, Mode02, Mode03, Mode04, Mode09

TEST_MODES = [
    ModeAT,
    Mode01,
    Mode02,
    Mode03,
    Mode04,

    Mode09,
]


@pytest.mark.parametrize(
    "mode",
    TEST_MODES,
)
def test_field_name_matches_command_name(mode):
    for field_name, field_value in mode.__dict__.items():
        if isinstance(field_value, Command):
            assert field_value.name == field_name, f"Field '{field_value.name}' does not match with the command name '{field_value.name}'."

@pytest.mark.parametrize(
    "mode",
    TEST_MODES,
)
def test_mins_maxs_units(mode):
    for command in mode.__dict__.values():
        if isinstance(command, Command):
            min_vals = command.min_values
            max_vals = command.max_values
            units = command.units

            if isinstance(max_vals, (list, tuple)) or isinstance(min_vals, (list, tuple)) or isinstance(units, (list, tuple)):
                assert isinstance(max_vals, (list, tuple)), f"Expected list/tuple for max_values, got {type(max_vals)}"
                assert isinstance(min_vals, (list, tuple)), f"Expected list/tuple for min_values, got {type(min_vals)}"
                assert isinstance(units, (list, tuple)), f"Expected list/tuple for units, got {type(units)}"

                # Ensure they have the same length
                assert len(max_vals) == len(min_vals) == len(units), f"Length mismatch: max={len(max_vals)}, min={len(min_vals)}, units={len(units)}"