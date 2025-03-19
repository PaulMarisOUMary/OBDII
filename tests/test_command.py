import pytest

from typing import Any, Dict

from obdii.basetypes import Command, Mode


@pytest.fixture
def arg_command_factory():
    """Fixture that returns a function to create Command instances."""
    def _create_command(pid: str, cmd_args: Dict[str, Any]) -> Command:
        return Command(
            mode=Mode.AT,
            pid=pid,
            n_bytes=0x02,
            name="Test Command",
            description="A command for testing",
            min_values=0,
            max_values=255,
            units='V',
            formula=None,
            command_args=cmd_args,
        )
    return _create_command


@pytest.mark.parametrize(
    "pid, command_args, arguments, expected_pid",
    [
        # Basic formatting tests
        ("TEST {h}", {'h': int}, [0], "TEST 0"),
        ("TEST {x} TEST {y}", {'x': int, 'y': int}, [0, 1], "TEST 0 TEST 1"),
        ("TEST {h}", {'h': int}, [10], "TEST A"),
        ("TEST {x} TEST {y}", {'x': int, 'y': int}, [10, 11], "TEST A TEST B"),
        
        # Hexadecimal formatting tests
        ("TEST {hh}", {"hh": int}, [0], "TEST 00"),
        ("TEST {xx} TEST {yy}", {"xx": int, "yy": int}, [0, 1], "TEST 00 TEST 01"),
        ("TEST {hh}", {"hh": int}, [10], "TEST 0A"),
        ("TEST {xx} TEST {yy}", {"xx": int, "yy": int}, [10, 11], "TEST 0A TEST 0B"),
        ("TEST {hh}", {"hh": int}, [17], "TEST 11"),
        ("TEST {xx} TEST {yy}", {"xx": int, "yy": int}, [17, 18], "TEST 11 TEST 12"),
        
        # Edge cases
        ("TEST {hh}", {"hh": int}, [255], "TEST FF"),
    ]
)
def test_command_correct_arguments(arg_command_factory, pid, command_args, arguments, expected_pid):
    command = arg_command_factory(pid, command_args)

    called_command = command(*arguments)

    assert called_command.is_formatted == True
    assert called_command.pid == expected_pid
    assert called_command.pid != command.pid


@pytest.mark.parametrize(
    "pid, command_args, arguments, expected_exception",
    [
        # Missing arguments
        ("TEST {h}", {'h': int}, [], ValueError),
        ("TEST {x} TEST {y}", {'x': int, 'y': int}, [1], ValueError),

        # Too many arguments
        ("TEST {x}", {'x': int}, [1, 2], ValueError),

        # Incorrect types
        ("TEST {h}", {'h': int}, ["string"], TypeError),
        ("TEST {xx}", {"xx": str}, [1], TypeError),
        ("TEST {xx}", {"xx": str}, [1.5], TypeError),

        # Argument formatting issues
        ("TEST {hh}", {"hh": int}, [256], ValueError),
        ("TEST {xx}", {"xx": str}, ["string"], ValueError),
        ("TEST {xx}", {"xx": str}, ["s"], ValueError),

        # Missing placeholders
        ("TEST", {'h': int}, [1], ValueError),
        ("TEST", {"xx": str, "yy": str}, ["ii", "jj"], ValueError),

        # Edge Cases
        ("TEST", {}, [], ValueError),
        ("TEST {h}", {}, [], ValueError),
        ("TEST {h}", {}, [1], ValueError),
        ("TEST {h}", {'h': int}, [None], TypeError),
        ("TEST {xx}", {"xx": str}, [None], TypeError),
        ("TEST {xx}", {"xx": str}, [''], ValueError),
        ("TEST {hh}", {"hh": int}, [-1], ValueError),
    ]
)
def test_command_invalid_arguments(arg_command_factory, pid, command_args, arguments, expected_exception):
    command = arg_command_factory(pid, command_args)

    with pytest.raises(expected_exception):
        command(*arguments)


@pytest.mark.parametrize(
    "pid, command_args, expected_query",
    [
        # 1. Basic Command
        (0x01, None, b"AT 01\r"),
        (0x01, {}, b"AT 01\r"),
        (0x0A, None, b"AT 0A\r"),
        (0xFF, {}, b"AT FF\r"),
        ("01", None, b"AT 01\r"),
        ("01", {}, b"AT 01\r"),
        ("TEST", None, b"AT TEST\r"),
        ("TEST", {}, b"AT TEST\r"),

        # 2. Missing Arguments (and Expected Errors)
        (0x01, {'h': int}, ValueError),
        ("01", {'h': int}, ValueError),
    ]
)
def test_build_function(arg_command_factory, pid, command_args, expected_query):
    command = arg_command_factory(pid, command_args)

    if isinstance(expected_query, bytes):
        query = command.build()
        assert query == expected_query
    else:
        with pytest.raises(expected_query):
            command.build()