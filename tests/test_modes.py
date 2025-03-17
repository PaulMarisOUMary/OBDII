import pytest

from obdii.basetypes import Command
from obdii.modes import ModeAT, Mode01, Mode02, Mode03, Mode04


@pytest.mark.parametrize(
    "mode",
    [
        ModeAT,
        Mode01,
        Mode02,
        Mode03,
        Mode04,
    ]
)
def test_field_name_matches_command_name(mode):
    for field_name, field_value in mode.__dict__.items():
        if isinstance(field_value, Command):
            assert field_value.name == field_name, f"Field '{field_value.name}' does not match with the command name '{field_value.name}'."