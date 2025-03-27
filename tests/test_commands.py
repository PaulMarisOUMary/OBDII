import pytest

from obdii.commands import Commands
from obdii.modes import Mode01, Mode02, Mode03, Mode04, Mode09


@pytest.mark.parametrize(
    "key, expected",
    [
        (1, Mode01()),
        (2, Mode02()),
        (3, Mode03()),
        (4, Mode04()),

        (9, Mode09()),

        (0, KeyError),
    ]
)
def test_commands_getitem_int(key, expected):
    commands = Commands()

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            commands[key]
    else:
        result = commands[key]

        assert result == expected


@pytest.mark.parametrize(
    "key, expected",
    [
        ("SUPPORTED_PIDS_A", Mode01().SUPPORTED_PIDS_A),

        ('', KeyError),
    ]
)
def test_commands_getitem_str(key, expected):
    commands = Commands()

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            commands[key]
    else:
        result = commands[key]

        assert result == expected


@pytest.mark.parametrize(
    "key_1, key_2, expected",
    [
        (1, 0, Mode01().SUPPORTED_PIDS_A),

        (0, 0, KeyError),
    ]
)
def test_commands_getitem_int_int(key_1, key_2, expected):
    commands = Commands()

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            commands[key_1][key_2]
    else:
        result = commands[key_1][key_2]

        assert result == expected