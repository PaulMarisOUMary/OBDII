"""
Unit tests for obdii.command.Template class.
"""
import pytest

from obdii.command import Template


@pytest.fixture
def simple_template():
    """Fixture that returns a simple template with one parameter."""
    return Template("AT {cmd}")


@pytest.fixture
def multi_template():
    """Fixture that returns a template with multiple parameters."""
    return Template("AT {cmd:str} {value:int}")


@pytest.fixture
def hex_template():
    """Fixture that returns a template with hex type specifiers."""
    return Template("AT {addr:hex2} {data:hex4}")


class TestTemplateInitialization:
    """Test Template initialization and parsing."""

    @pytest.mark.parametrize(
        ("template", "t_names", "t_types"),
        [
            ("AT", [], [None]),
            ("AT {cmd}", ["cmd"], [None]),
            ("AT {cmd:str}", ["cmd"], ["str"]),
            ("AT {cmd:int}", ["cmd"], ["int"]),
            ("AT {cmd:hex}", ["cmd"], ["hex"]),
            ("AT {a} {b} {c}", ['a', 'b', 'c'], [None, None, None]),
            ("AT {a:str} {b:int} {c:hex2}", ['a', 'b', 'c'], ["str", "int", "hex2"]),
            ("{a:hex2} {b:hex4} {c:hex8}", ['a', 'b', 'c'], ["hex2", "hex4", "hex8"]),
            ("AT { x : int } { y } { } {}", ['x', 'y'], ["int", None]),
        ],
        ids=[
            "no_placeholders",
            "single_placeholder",
            "single_string_placeholder",
            "single_int_placeholder",
            "single_hex_placeholder",
            "multiple_placeholders",
            "multiple_type_placeholders",
            "hex_placeholders",
            "different_spacing_with_fakeholders",
        ]
    )
    def test_template_definition(self, template, t_names, t_types):
        t = Template(template)

        assert t.template_names == t_names
        for param, expected_name, expected_type in zip(t.params, t_names, t_types):
            assert param["name"] == expected_name
            assert param["type"] == expected_type

    def test_duplicate_names_raises_error(self):
        with pytest.raises(ValueError):
            Template("AT {a} {b} {a}")


class TestTemplateSubstitution:
    """Test Template substitution with various argument types."""

    @pytest.mark.parametrize(
        ("template", "kwargs", "expected"),
        [
            ("AT {cmd}", {"cmd": "TEST"}, "AT TEST"),
            ("AT {cmd:str}", {"cmd": 123}, "AT 123"),
            ("AT {cmd:str}", {"cmd": "TEST"}, "AT TEST"),
            ("{a} {b} {c}", {'a': '1', 'b': 2, 'c': 0x03}, "1 2 3"),
            ("AT {cmd:int}", {"cmd": 42}, "AT 42"),
            ("AT {cmd:int}", {"cmd": 3.14}, "AT 3"),
            ("AT {cmd:int}", {"cmd": "42"}, "AT 42"),
        ],
        ids=[
            "str_default",
            "str_explicit_int",
            "str_explicit_str",
            "multiple_str",
            "int_int",
            "int_float",
            "int_str",
        ],
    )
    def test_substitute_kwargs_basic(self, template, kwargs, expected):
        t = Template(template)
        result = t.substitute(**kwargs)
        assert result == expected

    @pytest.mark.parametrize(
        ("template", "args", "expected"),
        [
            ("AT {cmd}", ("TEST",), "AT TEST"),
            ("AT {cmd:str}", (123,), "AT 123"),
            ("{a} {b} {c}", ('1', '2', '3'), "1 2 3"),
            ("AT {cmd:int}", (42,), "AT 42"),
            ("AT {a:int} {b:int}", (1, 2), "AT 1 2"),
        ],
        ids=[
            "str_default",
            "str_explicit",
            "multiple_str",
            "int_single",
            "int_multiple",
        ],
    )
    def test_substitute_args_basic(self, template, args, expected):
        t = Template(template)
        result = t.substitute(*args)
        assert result == expected

    @pytest.mark.parametrize(
        ("template", "kwargs", "expected"),
        [
            ("AT {addr:hex2}", {"addr": 0}, "AT 00"),
            ("AT {addr:hex2}", {"addr": 10}, "AT 0A"),
            ("AT {addr:hex2}", {"addr": 255}, "AT FF"),
            ("AT {addr:hex4}", {"addr": 0}, "AT 0000"),
            ("AT {addr:hex4}", {"addr": 255}, "AT 00FF"),
            ("AT {addr:hex4}", {"addr": 4095}, "AT 0FFF"),
            ("AT {addr:hex4}", {"addr": 65535}, "AT FFFF"),
            ("AT {a:hex1} {b:hex2} {c:hex4}", {'a': 5, 'b': 16, 'c': 256}, "AT 5 10 0100"),
            ("{a:hex8}", {'a': 4294967295}, "FFFFFFFF"),
        ],
        ids=[
            "hex2_zero",
            "hex2_ten",
            "hex2_max",
            "hex4_zero",
            "hex4_255",
            "hex4_4095",
            "hex4_max",
            "hex_mixed",
            "hex8_max",
        ],
    )
    def test_substitute_hex_types(self, template, kwargs, expected):
        t = Template(template)
        result = t.substitute(**kwargs)
        assert result == expected

    def test_substitute_with_fixture(self, simple_template):
        result = simple_template.substitute(cmd="TEST")
        assert result == "AT TEST"

    def test_substitute_multi_fixture_kwargs(self, multi_template):
        result = multi_template.substitute(cmd="SET", value=42)
        assert result == "AT SET 42"

    def test_substitute_multi_fixture_args(self, multi_template):
        result = multi_template.substitute("SET", 42)
        assert result == "AT SET 42"

    def test_substitute_hex_fixture(self, hex_template):
        result = hex_template.substitute(addr=255, data=4095)
        assert result == "AT FF 0FFF"

    def test_no_placeholders_returns_original(self):
        t = Template("AT TEST")
        result = t.substitute()
        assert result == "AT TEST"


class TestTemplateSubstitutionErrors:
    """Test Template substitution error cases."""

    def test_both_args_and_kwargs_raises(self, simple_template):
        with pytest.raises(ValueError):
            simple_template.substitute("TEST", cmd="TEST")

    def test_wrong_number_of_args_too_few(self, multi_template):
        with pytest.raises(ValueError):
            multi_template.substitute("SET")

    def test_wrong_number_of_args_too_many(self, multi_template):
        with pytest.raises(ValueError):
            multi_template.substitute("SET", 42, "extra")

    def test_missing_kwargs(self, multi_template):
        with pytest.raises(ValueError):
            multi_template.substitute(cmd="SET")

    def test_extra_kwargs(self, multi_template):
        with pytest.raises(ValueError):
            multi_template.substitute(cmd="SET", value=42, extra="arg")

    def test_wrong_kwarg_names(self, multi_template):
        with pytest.raises(ValueError):
            multi_template.substitute(wrong="SET", value=42)

    def test_unsupported_type_specifier(self):
        t = Template("AT {cmd:unsupported}")
        with pytest.raises(ValueError):
            t.substitute(cmd="TEST")


class TestTemplateCastFunction:
    """Test Template._cast internal function."""

    def test_cast_str(self):
        t = Template("{a}")
        match_dict, cast_fn = t._cast("str")
        assert match_dict == {}
        assert cast_fn({}, "test") == "test"
        assert cast_fn({}, 123) == "123"

    def test_cast_int(self):
        t = Template("{a}")
        match_dict, cast_fn = t._cast("int")
        assert match_dict == {}
        assert cast_fn({}, 42) == "42"
        assert cast_fn({}, 3.14) == '3'
        assert cast_fn({}, "42") == "42"

    def test_cast_hex2(self):
        t = Template("{a}")
        match_dict, cast_fn = t._cast("hex2")
        assert match_dict == {"width": '2'}
        assert cast_fn({"width": '2'}, 0) == "00"
        assert cast_fn({"width": '2'}, 10) == "0A"
        assert cast_fn({"width": '2'}, 255) == "FF"

    def test_cast_hex4(self):
        t = Template("{a}")
        match_dict, cast_fn = t._cast("hex4")
        assert match_dict == {"width": '4'}
        assert cast_fn({"width": '4'}, 0) == "0000"
        assert cast_fn({"width": '4'}, 255) == "00FF"

    def test_cast_hex_no_width(self):
        t = Template("{a}")
        match_dict, cast_fn = t._cast("hex")
        assert match_dict == {"width": ''}
        assert cast_fn({"width": ''}, 15) == 'F'

    def test_cast_invalid_type(self):
        t = Template("{a}")
        with pytest.raises(ValueError, match="Unsupported type specifier"):
            t._cast("invalid")


class TestTemplateEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_string_template(self):
        t = Template('')
        assert t.template == ''
        assert t.template_names == []
        assert t.substitute() == ''

    def test_template_with_special_chars(self):
        t = Template("AT-{cmd}:{value}")
        result = t.substitute(cmd="TEST", value="OK")
        assert result == "AT-TEST:OK"

    def test_consecutive_placeholders(self):
        t = Template("{a}{b}{c}")
        result = t.substitute(a='1', b='2', c='3')
        assert result == "123"

    def test_placeholder_at_start(self):
        t = Template("{cmd} AT")
        result = t.substitute(cmd="TEST")
        assert result == "TEST AT"

    def test_placeholder_at_end(self):
        t = Template("AT {cmd}")
        result = t.substitute(cmd="TEST")
        assert result == "AT TEST"

    def test_only_placeholder(self):
        t = Template("{cmd}")
        result = t.substitute(cmd="TEST")
        assert result == "TEST"

    def test_hex_with_large_numbers(self):
        t = Template("{a:hex8}")
        result = t.substitute(a=305419896)
        assert result == "12345678"

    def test_int_conversion_from_float(self):
        t = Template("{a:int}")
        result = t.substitute(a=3.99)
        assert result == '3'

    def test_str_preserves_value(self):
        t = Template("{a:str}")
        result = t.substitute(a="  spaces  ")
        assert result == "  spaces  "

    def test_multiple_same_type(self):
        t = Template("{a:hex2} {b:hex2} {c:hex2}")
        result = t.substitute(a=1, b=2, c=3)
        assert result == "01 02 03"

    def test_mixed_positional_order_matters(self):
        t = Template("{first} {second} {third}")
        result = t.substitute('A', 'B', 'C')
        assert result == "A B C"
