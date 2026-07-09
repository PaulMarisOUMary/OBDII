"""
Unit tests for obdii.utils.bits module.
"""
import pytest

from obdii.utils.bits import (
    bytes_to_string,
    filter_bytes,
    hex_to_ints,
    hex_byte_length,
)


class TestHexToInts:
    """Test suite for hex_to_ints function."""

    @pytest.mark.parametrize(
        ("data", "expected"),
        [
            (b"ABCD", [0xAB, 0xCD]),
            (b"0ABC", [0x0A, 0xBC]),
            (b"0000", [0x00, 0x00]),
        ],
        ids=["four_bytes", "leading_zero", "double_zero"]
    )
    def test_odd_length_bytes(self, data, expected):
        """Test bytes."""
        result = hex_to_ints(data)
        
        assert result == expected
        assert all(0 <= chunk < 2**8 for chunk in result)

    def test_empty_bytes(self):
        """Test empty bytes."""
        result = hex_to_ints(b'')
        
        assert result == []
        assert isinstance(result, list)


class TestHexByteLength:
    """Test suite for hex_byte_length function."""

    def test_empty_string_returns_zero(self):
        """Test that an empty string returns 0 bytes."""
        result = hex_byte_length('')

        assert result == 0
        assert isinstance(result, int)

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (0x00, 1),
            (0x0C, 1),
            (0x1A, 1),
            (0xFF, 1),
        ],
        ids=[
            "zero",
            "engine_coolant_temp_pid",
            "single_hex_digit_value",
            "max_single_byte",
        ],
    )
    def test_single_byte_int(self, value, expected):
        """Test int values that fit in a single hex-encoded byte."""
        result = hex_byte_length(value)

        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (0x8220, 2),
            (0x9023, 2),
            (0x0100, 2),
            (0xFFFF, 2),
        ],
        ids=[
            "honda_atf_temp_8220",
            "honda_atf_temp_9023",
            "leading_zero_byte",
            "max_two_bytes",
        ],
    )
    def test_two_byte_int(self, value, expected):
        """Test int values spanning two hex-encoded bytes."""
        result = hex_byte_length(value)

        assert result == expected

    def test_three_byte_int(self):
        """Test an int value spanning three hex-encoded bytes."""
        result = hex_byte_length(0xFFFFFF)

        assert result == 3

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("0C", 1),
            ("00", 1),
            ("FF", 1),
        ],
        ids=["single_byte_hex_string", "zero_hex_string", "max_single_byte_hex_string"],
    )
    def test_single_byte_str(self, value, expected):
        """Test pre-formatted single-byte hex strings."""
        result = hex_byte_length(value)

        assert result == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("8220", 2),
            ("9023", 2),
            ("0100", 2),
        ],
        ids=[
            "honda_atf_temp_8220_str",
            "honda_atf_temp_9023_str",
            "leading_zero_byte_str",
        ],
    )
    def test_two_byte_str(self, value, expected):
        """Test pre-formatted two-byte hex strings."""
        result = hex_byte_length(value)

        assert result == expected

    @pytest.mark.parametrize(
        ("int_value", "str_value"),
        [
            (0x0C, "0C"),
            (0x8220, "8220"),
            (0x00, "00"),
        ],
        ids=["single_byte_pid", "two_byte_pid", "zero_pid"],
    )
    def test_int_and_str_agree(self, int_value, str_value):
        """Test that an int and its pre-formatted hex string equivalent agree."""
        assert hex_byte_length(int_value) == hex_byte_length(str_value)

    def test_odd_length_hex_string_rounds_up(self):
        """Test that an odd-length hex string still rounds up to a whole byte."""
        result = hex_byte_length("ABC")

        assert result == 2


class TestFilterBytes:
    """Test suite for filter_bytes function."""

    @pytest.mark.parametrize(
        ("data", "patterns", "expected"),
        [
            (b"AB CD EF", (b' ',), b"ABCDEF"),
            (b"A>B>C>D>", (b'>',), b"ABCD"),
            (b"Hello\nWorld", (b'\n',), b"HelloWorld"),
            (b"Test\rData", (b'\r',), b"TestData"),
            (b"A\tB\tC", (b'\t',), b"ABC"),
        ],
        ids=["remove_spaces", "remove_prompt", "remove_newline", "remove_carriage", "remove_tab"],
    )
    def test_single_pattern_removal(self, data, patterns, expected):
        """Test removing single pattern from bytes."""
        result = filter_bytes(data, *patterns)
        assert result == expected

    @pytest.mark.parametrize(
        ("data", "patterns", "expected"),
        [
            (b"AB\r\nCD\r\nEF", (b'\r', b'\n'), b"ABCDEF"),
            (b"A B>C D>", (b' ', b'>'), b"ABCD"),
            (b"Test\r\n\tData", (b'\r', b'\n', b'\t'), b"TestData"),
        ],
        ids=["remove_crlf", "remove_space_and_prompt", "remove_whitespace"],
    )
    def test_multiple_patterns_removal(self, data, patterns, expected):
        """Test removing multiple patterns from bytes."""
        result = filter_bytes(data, *patterns)
        assert result == expected

    def test_no_patterns_returns_original(self):
        """Test with no patterns - should return original."""
        data = b"ABCDEF"
        result = filter_bytes(data)
        
        assert result == data
        assert result is data

    def test_pattern_not_present(self):
        """Test removing pattern that doesn't exist."""
        data = b"ABCDEF"
        result = filter_bytes(data, b"XYZ")
        
        assert result == data

    def test_empty_data(self):
        """Test filtering empty bytes."""
        result = filter_bytes(b'', b' ')
        assert result == b''

    @pytest.mark.parametrize(
        ("data", "pattern", "expected"),
        [
            (b"A B C D E", b' ', b"ABCDE"),
            (b">>>>>", b'>', b''),
            (b"AAAAABBBBB", b'A', b"BBBBB"),
            (b"AAAA", b"AA", b''),
            (b"ABABAB", b"AB", b''),
        ],
        ids=["multiple_spaces", "all_prompts", "consecutive_chars", "double_pattern", "repeating_pattern"],
    )
    def test_multiple_occurrences(self, data, pattern, expected):
        """Test removing multiple occurrences of pattern."""
        result = filter_bytes(data, pattern)
        assert result == expected

    def test_multi_char_pattern(self):
        """Test multi-character pattern removal."""
        result = filter_bytes(b"AB<<>>CD<<>>EF", b"<<>>")
        assert result == b"ABCDEF"

    def test_empty_pattern_returns_original(self):
        """Test that empty pattern returns original data."""
        data = b"ABCDEF"
        result = filter_bytes(data, b'')
        assert result == data

    def test_overlapping_patterns(self):
        """Test removing overlapping patterns."""
        result = filter_bytes(b"AABBCC", b"BB", b"CC")
        assert result == b"AA"


class TestBytesToString:
    """Test suite for bytes_to_string function."""

    @pytest.mark.parametrize(
        ("data", "expected"),
        [
            (b"Hello World", "Hello World"),
            (b"AABBCCDD", "AABBCCDD"),
            (b"12345", "12345"),
            (b"ELM327", "ELM327"),
            (b"Test", "Test"),
        ],
        ids=["simple_text", "hex_string", "numbers", "elm_version", "single_word"],
    )
    def test_simple_ascii_bytes(self, data, expected):
        """Test converting simple ASCII bytes."""
        result = bytes_to_string(data)
        
        assert result == expected
        assert isinstance(result, str)

    @pytest.mark.parametrize(
        ("data", "expected"),
        [
            (b"  Hello World  ", "Hello World"),
            (b"\nHello\n", "Hello"),
            (b"\tHello\t", "Hello"),
            (b"   \n\t\r   ", ''),
            (b"  ELM327 v1.5  ", "ELM327 v1.5"),
            (b"\r\n\r\nTest\r\n", "Test"),
        ],
        ids=["spaces", "newlines", "tabs", "only_whitespace", "mixed_whitespace", "crlf"],
    )
    def test_bytes_with_whitespace(self, data, expected):
        """Test bytes with leading/trailing whitespace."""
        result = bytes_to_string(data)
        assert result == expected

    def test_empty_bytes(self):
        """Test empty bytes returns empty string."""
        result = bytes_to_string(b'')
        
        assert result == ''
        assert isinstance(result, str)

    def test_invalid_utf8_bytes(self):
        """Test bytes with invalid UTF-8 sequences."""
        result = bytes_to_string(b"Hello\xFF\xFEWorld")
        
        # Should ignore errors and decode what it can
        assert "Hello" in result
        assert "World" in result

    @pytest.mark.parametrize(
        "data",
        [
            b"41 0C 1A F8",
            b"7E8 03 41 0C 1A F8",
            b'>',
            b"NO DATA",
            b"OK",
            b"SEARCHING...",
            b"BUS INIT: OK",
            b'?',
            b"UNABLE TO CONNECT",
        ],
        ids=[
            "obd_response",
            "can_response",
            "prompt",
            "no_data",
            "ok",
            "searching",
            "bus_init",
            "error",
            "unable_connect",
        ],
    )
    def test_obd_common_responses(self, data):
        """Test common OBD-II response patterns."""
        result = bytes_to_string(data)
        
        assert isinstance(result, str)
        assert len(result) > 0

    def test_null_bytes_in_data(self):
        """Test bytes containing null characters."""
        result = bytes_to_string(b"Test\x00Data")
        assert isinstance(result, str)
        # Null bytes should be handled gracefully

    def test_only_null_bytes(self):
        """Test bytes with only null characters."""
        result = bytes_to_string(b"\x00\x00\x00")
        assert isinstance(result, str)