import pytest

from obdii.basetypes import _MissingSentinel, MISSING


missing_test_cases = [
    (_MissingSentinel(), True),
    (object(), False),
    (42, False),
]


@pytest.mark.parametrize("obj, expected", missing_test_cases)
def test_missing_eq_operator(obj, expected):
    assert (MISSING == obj) is expected, f"Expected MISSING == {obj} to be {expected}"


@pytest.mark.parametrize("obj, expected", missing_test_cases)
def test_missing_is_operator(obj, expected):
    assert (MISSING is obj) is expected, f"Expected MISSING is {obj} to be {expected}"


def test_missing_singleton_behavior():
    assert MISSING is _MissingSentinel(), "MISSING is not the singleton instance"

    missing1 = _MissingSentinel()
    missing2 = _MissingSentinel()

    assert missing1 is missing2, "MISSING instances are not the same"


@pytest.mark.parametrize("obj, expected_repr", [
    (MISSING, "..."),
    (_MissingSentinel(), "..."),
])
def test_missing_repr(obj, expected_repr):
    assert repr(obj) == expected_repr, f"Expected repr({obj}) to be '{expected_repr}'"


@pytest.mark.parametrize("obj, expected_bool", [
    (MISSING, False),
    (_MissingSentinel(), False),
])
def test_missing_bool(obj, expected_bool):
    assert bool(obj) is expected_bool, f"Expected bool({obj}) to be {expected_bool}"


@pytest.mark.parametrize("obj, expected_hash", [
    (MISSING, 0),
    (_MissingSentinel(), 0),
])
def test_missing_hash(obj, expected_hash):
    assert hash(obj) == expected_hash, f"Expected hash({obj}) to be {expected_hash}"