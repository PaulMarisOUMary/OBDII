from ast import (
    Add,
    Sub,
    Mult,
    Div,
    FloorDiv,
    Mod,
    Pow,
    BitXor,
    UAdd,
    USub,
    parse,
    NodeVisitor,
    Expr,
    BinOp,
    UnaryOp,
    Name,
    Constant,
)
from typing import List, Any, NoReturn
from operator import add, sub, mul, truediv, floordiv, mod, pow, xor

from ..basetypes import BytesRows, Real


class SafeEvaluator(NodeVisitor):
    """A safe evaluator that only allows basic math operations."""

    operators = {
        Add: add,
        Sub: sub,
        Mult: mul,
        Div: truediv,
        FloorDiv: floordiv,
        Mod: mod,
        Pow: pow,
        BitXor: xor,
    }

    def __init__(self, variables):
        self.variables = variables

    def visit_BinOp(self, node: BinOp) -> Any:
        return self.operators[type(node.op)](
            self.visit(node.left), self.visit(node.right)
        )

    def visit_UnaryOp(self, node: UnaryOp) -> Any:
        operand = self.visit(node.operand)
        if isinstance(node.op, UAdd):
            return +operand
        elif isinstance(node.op, USub):
            return -operand
        raise ValueError("Unsupported operation")

    def visit_Name(self, node: Name) -> Any:
        if node.id in self.variables:
            return self.variables[node.id]
        raise ValueError(f"Unknown variable: {node.id}")

    def visit_Constant(self, node: Constant) -> Any:
        return node.value

    def visit_Expr(self, node: Expr) -> Any:
        return self.visit(node.value)

    def generic_visit(self, node) -> NoReturn:
        raise ValueError("Unsupported operation in formula")


class Formula:
    """
    Represents a mathematical formula based on a string expression.

    Example
    -------
    .. code-block:: python3

        # 0B (hex) | 11 (dec) -> A
        # 40 (hex) | 64 (dec) -> B
        parsed_data = [(b'0B', b'40')]

        formula = Formula("(256*A+B)/4")
        result = formula(parsed_data)
        # (256 * 11 + 64)/4

        >>> result
        720.0
    """

    def __init__(self, expression: str):
        """
        Initialize the Formula with a given expression.

        Parameters
        ----------
        expression: :class:`str`
            The expression string to evaluate. Variable names are converted to uppercase.
        """
        self.expression = expression.upper()

        self.parsed_expr = parse(self.expression, mode="eval")

    def __call__(self, parsed_data: BytesRows) -> Real:
        """
        Evaluate the formula on the given parsed_data.

        Parameters
        ----------
        parsed_data: :class:`BytesRows`
            The parsed data to evaluate the formula against.
        """
        if not parsed_data or not parsed_data[0]:
            raise ValueError(
                "Invalid parsed_data: must contain at least one non-empty list."
            )

        first_item = parsed_data[0]

        values = {
            chr(ord('A') + i): int(first_item[i], 16) for i in range(len(first_item))
        }

        evaluator = SafeEvaluator(values)
        return evaluator.visit(self.parsed_expr.body)


class MultiFormula:
    """
    Represents multiple mathematical formulas based on string expressions.

    Example
    -------
    .. code-block:: python3

        # 8F (hex) | 143 (dec) -> A
        # 7D (hex) | 125 (dec) -> B
        # 95 (hex) | 149 (dec) -> C
        # 80 (hex) | 128 (dec) -> D
        # 6F (hex) | 111 (dec) -> E
        parsed_data = [(b"8F", b"7D", b"95", b"80", b"6F")]

        engine_torque = MultiFormula("A-125", "B-125", "C-125", "D-125", "E-125")
        result = engine_torque(parsed_data)

        >>> result
        [18, 0, 24, 3, -14]
    """

    def __init__(self, *expressions: str) -> None:
        """
        Initialize formulas based on given expressions.

        Parameters
        ----------
        *expressions: :class:`str`
            Expression strings to evaluate. Variable names are converted to uppercase.
        """
        self.formulas = [Formula(expr) for expr in expressions]

    def __call__(self, parsed_data: BytesRows) -> List[Real]:
        """
        Evaluate all formulas on the given parsed_data.

        Parameters
        ----------
        parsed_data: :class:`BytesRows`
            The parsed data to evaluate the formulas against.
        """
        return [formula(parsed_data) for formula in self.formulas]
