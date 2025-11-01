"""
Unit tests for obdii.utils.bits module.
"""
import pytest

from obdii.utils.bits import (
    split_hex_bytes,
    is_bytes_hex,
    filter_bytes,
    bytes_to_string,
)


class TestSplitHexBytes:
    """Test suite for split_hex_bytes function."""

    @pytest.mark.parametrize(
        ("data", "expected"),
        [
            (b"AABBCCDD", (b"AA", b"BB", b"CC", b"DD")),
            (b"0123456789ABCDEF", (b"01", b"23", b"45", b"67", b"89", b"AB", b"CD", b"EF")),
            (b"AB", (b"AB",)),
            (b"00", (b"00",)),
            (b"FF", (b"FF",)),
        ],
        ids=["four_bytes", "eight_bytes", "one_pair", "zero_pair", "max_byte"]
    )
    def test_even_length_bytes(self, data, expected):
        """Test splitting bytes with even length."""
        result = split_hex_bytes(data)
        
        assert result == expected
        assert all(len(chunk) == 2 for chunk in result)

    @pytest.mark.parametrize(
        ("data", "expected"),
        [
            (b"ABC", (b"0A", b"BC")),
            (b'F', (b"0F",)),
            (b"12345", (b"01", b"23", b"45")),
            (b"ABCDE", (b"0A", b"BC", b"DE")),
            (b'1', (b"01",)),
            (b'9', (b"09",)),
        ],
        ids=["three_chars", "single_F", "five_digits", "five_hex", "single_1", "single_9"]
    )
    def test_odd_length_bytes(self, data, expected):
        """Test splitting bytes with odd length - should prepend '0'."""
        result = split_hex_bytes(data)
        
        assert result == expected
        assert all(len(chunk) == 2 for chunk in result)

    def test_empty_bytes(self):
        """Test splitting empty bytes."""
        result = split_hex_bytes(b'')
        
        assert result == ()
        assert isinstance(result, tuple)


class TestIsBytesHex:
    """Test suite for is_bytes_hex function."""

    @pytest.mark.parametrize(
        "data",
        [
            b"ABCDEF",
            b"0123456789",
            b"DEADBEEF",
            b"abcdef",
            b"AbCdEf",
            b"0a1B2c3D",
            b'A',
            b'0',
            b'f',
            b"FF",
            b"aBcDeF0123456789",  # Long mixed case
            b"00000000",  # All zeros
            b"FFFFFFFF",  # All max
        ],
        ids=[
            "uppercase",
            "numbers",
            "deadbeef",
            "lowercase",
            "mixed_case",
            "mixed_numbers",
            "single_A",
            "single_0",
            "single_f",
            "double_F",
            "long_mixed",
            "all_zeros",
            "all_max",
        ],
    )
    def test_valid_hex_bytes(self, data):
        """Test valid hexadecimal bytes."""
        assert is_bytes_hex(data) is True

    @pytest.mark.parametrize(
        "data",
        [
            b'',
            b"GHIJK",
            b"12XY34",
            b"ABC DEF",
            b"!@#$%",
            b"AB\r\nCD",
            b"AB CD",
            b"0x12",
            b"AB-CD",
            b"AB:CD",
            b'g',
            b'Z',
            b"\x00\x01",  # Binary data
        ],
        ids=[
            "empty",
            "invalid_letters",
            "mixed_invalid",
            "with_space",
            "special_chars",
            "with_newlines",
            "hex_with_space",
            "hex_prefix",
            "with_dash",
            "with_colon",
            "invalid_g",
            "invalid_Z",
            "binary_data",
        ],
    )
    def test_invalid_hex_bytes(self, data):
        """Test invalid hexadecimal bytes."""
        assert is_bytes_hex(data) is False


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