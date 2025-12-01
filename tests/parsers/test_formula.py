"""
Unit tests for obdii.parsers.formula module.
"""
import pytest

from ast import parse

from obdii.parsers.formula import Formula, MultiFormula, SafeEvaluator


@pytest.mark.parametrize(
    ("expression", "variables", "expected"),
    [
        ("a + b", {'a': 1, 'b': 2}, 3),
        ("a - b", {'a': 3, 'b': 1}, 2),
        ("a * b", {'a': 2, 'b': 3}, 6),
        ("a / b", {'a': 6, 'b': 2}, 3),
        ("a // b", {'a': 7, 'b': 3}, 2),
        ("a % b", {'a': 7, 'b': 3}, 1),
        ("a ** b", {'a': 2, 'b': 3}, 8),
        ("a ^ b", {'a': 5, 'b': 3}, 6),
    ],
    ids=["add", "sub", "mul", "truediv", "floordiv", "mod", "pow", "xor"],
)
def test_safe_evaluator(expression, variables, expected):
    evaluator = SafeEvaluator(variables)
    node = parse(expression, mode="eval")
    result = evaluator.visit(node.body)
    assert result == expected


@pytest.mark.parametrize(
    ("expression", "parsed", "expected"),
    [
        ("a + b", [['1', '2']], 3),
        ("a - b", [['3', '1']], 2),
        ("a * b", [['2', '3']], 6),
        ("a / b", [['6', '2']], 3),

        ("a + b", [['1', 'A']], 11),
        ("a - b", [['A', '5']], 5),
        ("a * b", [['A', '3']], 30),
        ("a / b", [['A', '2']], 5),

        ("a + b", [['1', "AB"]], 172),
        ("a - b", [["AB", '9']], 162),
        ("a * b", [["AB", '4']], 684),
        ("a / b", [["AC", '2']], 86),
    ],
    ids=[
        "dec_add", "dec_sub", "dec_mul", "dec_div",
        "hex_add", "hex_sub", "hex_mul", "hex_div",
        "mix_add", "mix_sub", "mix_mul", "mix_div",
    ],
)
def test_formula(expression, parsed, expected):
    fn = Formula(expression)
    result = fn(parsed)
    assert result == expected


@pytest.mark.parametrize(
    ("expression", "parsed", "expected"),
    [
        ("(a + b) * c", [['1', '2', '3']], 9),
        ("a + (b * c)", [['1', '2', '3']], 7),
        ("(a + b) - (c / d)", [['1', '2', '3', '1']], 0),
        ("a + (b - c) * d", [['6', '4', '2', '3']], 12),
        ("(a - b) * (c + d)", [['8', '4', '2', '2']], 16),
        ("(a + (b * c)) - d", [['1', '2', '3', '4']], 3),
        ("(a * (b + c)) - d", [['2', '3', '4', '1']], 13),
        ("(a + b) * (c + (d - e))", [['1', '2', '3', '4', '5']], 6),

        ('c', [['1', '2', '3']], 3),
    ],
    ids=["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "var_only"],
)
def test_formula_with_parentheses(expression, parsed, expected):
    fn = Formula(expression)
    result = fn(parsed)
    assert result == expected


def test_formula_invalid_input():
    fn = Formula("a + b")
    with pytest.raises(ValueError):
        fn([])


@pytest.mark.parametrize(
    ("expressions", "parsed", "expected", "expected_exc"),
    [
        (['a', 'b', 'c'], [['1', '2', '3']], [1, 2, 3], None),
        (['a', 'b', 'c'], [['A', 'B', 'C']], [10, 11, 12], None),

        (["a + b", "c - a"], [['1', '2', '3']], [3, 2], None),
        (["a + b", "c - a"], [['A', 'B', 'C']], [21, 2], None),

        (["a * 2", "b / 2"], [['8', 'A']], [16, 5], None),
        (["(a + b) * c", "a - (b / c)"], [['1', '2', '4']], [12, 0.5], None),
        (["a + b", "c * 2"], [['A', '5', '8']], [15, 16], None),
        (["a * (b + c)", "(a + b) / c"], [['2', '3', '1']], [8, 5], None),

        (["a + b"], [['4', '2']], [6], None),

        (["a + b", "c - d"], [[]], None, ValueError),
        (['a', 'b', 'c', "d * 10"], [['A', 'B']], None, ValueError),

        (['c'], [['1', '2', '3']], [3], None),
    ],
    ids=[
        "vars_123", "vars_ABC",
        "ops_simple_dec", "ops_simple_hex",
        "ops_scale_mix", "ops_paren_div", "ops_mix_add_mul", "ops_mix_nested",
        "single_expr",
        "error_empty_parsed", "error_args_mismatch",
        "single_c",
    ],
)
def test_multi_formula(expressions, parsed, expected, expected_exc):
    mf = MultiFormula(*expressions)
    if expected_exc:
        with pytest.raises(expected_exc):
            _ = mf(parsed)
        return
    result = mf(parsed)
    assert result == expected