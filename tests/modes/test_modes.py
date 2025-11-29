"""
Unit tests for obdii.modes.mode_* modules.
"""
import pytest

from ast import Assign, Name, parse, walk
from inspect import getsource

from obdii.command import Command
from obdii.modes import ModeAT, Mode01, Mode02, Mode03, Mode04, Mode09

TEST_MODES = [
    ModeAT,
    Mode01,
    Mode02,
    Mode03,
    Mode04,

    Mode09,
]

TEST_MODES_ids = ["AT", "01", "02", "03", "04", "09"]


@pytest.mark.parametrize(
    "mode",
    TEST_MODES,
    ids=TEST_MODES_ids,
)
def test_field_name_matches_command_name(mode):
    for field_name, field_value in vars(mode).items():
        if isinstance(field_value, Command):
            assert field_value.name == field_name, f"Field '{field_value.name}' does not match with the command name '{field_value.name}'."

@pytest.mark.parametrize(
    "mode",
    TEST_MODES,
    ids=TEST_MODES_ids,
)
def test_mins_maxs_units(mode):
    for command in vars(mode).values():
        if not isinstance(command, Command):
            continue

        min_vals = command.min_values
        max_vals = command.max_values
        units = command.units

        if isinstance(max_vals, (list, tuple)) or isinstance(min_vals, (list, tuple)) or isinstance(units, (list, tuple)):
            assert isinstance(max_vals, (list, tuple))
            assert isinstance(min_vals, (list, tuple))
            assert isinstance(units, (list, tuple))
            assert len(max_vals) == len(min_vals) == len(units)


@pytest.mark.parametrize(
    "mode",
    TEST_MODES,
    ids=TEST_MODES_ids,
)
def test_for_unique_fields(mode):
    source = getsource(mode)
    tree = parse(source)
    assignments = {}
    duplicates = []

    for node in walk(tree):
        if isinstance(node, Assign):
            for target in node.targets:
                if isinstance(target, Name):
                    var_name = target.id
                    if var_name in assignments:
                        duplicates.append(var_name)
                    assignments[var_name] = True
    
    assert not duplicates, f"Duplicate field(s) defined in {mode.__name__}: {', '.join(duplicates)}"

@pytest.mark.parametrize(
    "mode",
    TEST_MODES,
    ids=TEST_MODES_ids,
)
def test_missing_formula(mode):
    for command in vars(mode).values():
        if (
            isinstance(command, Command)
            and not command.resolver
        ):
            print(f"Missing Formula for: {command.name}")