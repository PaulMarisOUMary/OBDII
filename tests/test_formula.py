import pytest

from ast import parse

from obdii.formula import Formula, SafeEvaluator


@pytest.mark.parametrize(
    "expression, variables, expected_result",
    [
        ("a + b", {"a": 1, "b": 2}, 3),
        ("a - b", {"a": 3, "b": 1}, 2),
        ("a * b", {"a": 2, "b": 3}, 6),
        ("a / b", {"a": 6, "b": 2}, 3),
        ("a // b", {"a": 7, "b": 3}, 2),
        ("a % b", {"a": 7, "b": 3}, 1),
        ("a ** b", {"a": 2, "b": 3}, 8),
        ("a ^ b", {"a": 5, "b": 3}, 6),
    ]
)
def test_safe_evaluator(expression, variables, expected_result):
    evaluator = SafeEvaluator(variables)

    parsed_expr = parse(expression, mode="eval")
    result = evaluator.visit(parsed_expr.body)

    assert result == expected_result


@pytest.mark.parametrize(
    "expression, parsed_data, expected_result",
    [
        ("a + b", [["1", "2"]], 3),
        ("a - b", [["3", "1"]], 2),
        ("a * b", [["2", "3"]], 6),
        ("a / b", [["6", "2"]], 3),

        ("a + b", [["1", "A"]], 11),
        ("a - b", [["A", "5"]], 5),
        ("a * b", [["A", "3"]], 30),
        ("a / b", [["A", "2"]], 5),

        ("a + b", [["1", "AB"]], 172),
        ("a - b", [["AB", "9"]], 162),
        ("a * b", [["AB", "4"]], 684),
        ("a / b", [["AC", "2"]], 86),
    ]
)
def test_formula(expression, parsed_data, expected_result):
    formula = Formula(expression)

    result = formula(parsed_data)

    assert result == expected_result


@pytest.mark.parametrize(
    "expression, parsed_data, expected_result",
    [
        ("(a + b) * c", [["1", "2", "3"]], 9),
        ("a + (b * c)", [["1", "2", "3"]], 7),
        ("(a + b) - (c / d)", [["1", "2", "3", "1"]], 0),
        ("a + (b - c) * d", [["6", "4", "2", "3"]], 12),
        ("(a - b) * (c + d)", [["8", "4", "2", "2"]], 16),
        ("(a + (b * c)) - d", [["1", "2", "3", "4"]], 3),
        ("(a * (b + c)) - d", [["2", "3", "4", "1"]], 13),
        ("(a + b) * (c + (d - e))", [["1", "2", "3", "4", "5"]], 6),
    ]
)
def test_formula_with_parentheses(expression, parsed_data, expected_result):
    formula = Formula(expression)

    result = formula(parsed_data)

    assert result == expected_result


def test_formula_invalid_input():
    formula = Formula("a + b")

    with pytest.raises(ValueError):
        formula([])
