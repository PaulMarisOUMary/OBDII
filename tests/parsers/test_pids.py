"""
Unit tests for obdii.parsers.pids module.
"""
import pytest

from obdii.parsers.pids import SupportedPIDS, EnumeratedPIDS

@pytest.mark.parametrize(
    ("base_pid, parsed_data, expected, expected_exc"),
    # e.g.
    # B    E    1    F    A    8    1    3
    # 1011 1110 0001 1111 1010 1000 0001 0011
    [
        (0x01, [], None, ValueError),
        (0x01, [0xBE, 0x1F, 0xA8, 0x13], [0x01, 0x03, 0x04, 0x05, 0x06, 0x07, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x13, 0x15, 0x1C, 0x1F, 0x20], None),
        (0x21, [0x80, 0x01, 0xA0, 0x01, 0x90, 0x15, 0xB0, 0x15], [33, 48, 49, 51, 64, 65, 68, 76, 78, 80, 81, 83, 84, 92, 94, 96], None)
    ],
    ids=["empty", "wiki_example", "multiple_rows"],
)
def test_supported_pids(base_pid, parsed_data, expected, expected_exc):
    """Test SupportedPIDS parses bit patterns correctly."""
    sp = SupportedPIDS(base_pid)
    if expected_exc:
        with pytest.raises(expected_exc):
            sp(parsed_data)
    else:
        result = sp(parsed_data)
        assert result == expected

@pytest.mark.parametrize(
    ("mapping, parsed_data, expected"),
    [
        (
            {0: "Off", 1: "On"},
            [0x00],
            [(0, "Off")],
        ),
        (
            {0: "Off", 1: "On"},
            [0x01],
            [(1, "On")],
        ),
        (
            {0: "Off", 1: "On"},
            [0x00, 0x01],
            [(0, "Off"), (1, "On")],
        ),
        (
            {2: 'B', 3: 'C'},
            [0x0F, 0x02],
            [(15, None), (2, 'B')],
        ),
        (
            {0: "Zero", 255: "Max"},
            [0x00, 0xFF],
            [(0, "Zero"), (255, "Max")],
        ),
    ],
    ids=["single_off", "single_on", "both_values", "sparse_keys", "extreme_keys"],
)
def test_enumerated_pids(mapping, parsed_data, expected):
    """Test EnumeratedPIDS maps values to descriptions."""
    ep = EnumeratedPIDS(mapping)
    result = ep(parsed_data)
    assert result == expected
