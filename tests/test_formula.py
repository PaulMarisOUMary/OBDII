import pytest

from ast import parse

from obdii.formula import Formula, MultiFormula, SafeEvaluator


@pytest.mark.parametrize(
    "expression, variables, expected_result",
    [
        ("a + b", {'a': 1, 'b': 2}, 3),
        ("a - b", {'a': 3, 'b': 1}, 2),
        ("a * b", {'a': 2, 'b': 3}, 6),
        ("a / b", {'a': 6, 'b': 2}, 3),
        ("a // b", {'a': 7, 'b': 3}, 2),
        ("a % b", {'a': 7, 'b': 3}, 1),
        ("a ** b", {'a': 2, 'b': 3}, 8),
        ("a ^ b", {'a': 5, 'b': 3}, 6),
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
    ]
)
def test_formula(expression, parsed_data, expected_result):
    formula = Formula(expression)

    result = formula(parsed_data)

    assert result == expected_result


@pytest.mark.parametrize(
    "expression, parsed_data, expected_result",
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


@pytest.mark.parametrize(
    "expressions, parsed_data, expected_results",
    [
        (['a', 'b', 'c'], [['1', '2', '3']], [1, 2, 3]),
        (['a', 'b', 'c'], [['A', 'B', 'C']], [10, 11, 12]),

        (["a + b", "c - a"], [['1', '2', '3']], [3, 2]),
        (["a + b", "c - a"], [['A', 'B', 'C']], [21, 2]),

        (["a * 2", "b / 2"], [['8', 'A']], [16, 5]),
        (["(a + b) * c", "a - (b / c)"], [['1', '2', '4']], [12, 0.5]),
        (["a + b", "c * 2"], [['A', '5', '8']], [15, 16]),
        (["a * (b + c)", "(a + b) / c"], [['2', '3', '1']], [8, 5]),

        (["a + b"], [['4', '2']], [6]),

        (["a + b", "c - d"], [[]], pytest.raises(ValueError)),
        (['a', 'b', 'c', "d * 10"], [['A', 'B']], pytest.raises(ValueError)),

        (['c'], [['1', '2', '3']], [3]),
    ]
)
def test_multi_formula(expressions, parsed_data, expected_results):
    multi_formula = MultiFormula(*expressions)

    if isinstance(expected_results, list):
        result = multi_formula(parsed_data)
        assert result == expected_results
    else:
        with expected_results:
            multi_formula(parsed_data)