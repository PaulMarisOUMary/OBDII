from ast import (
    Add, Sub, Mult, Div, FloorDiv, Mod, Pow, BitXor, UAdd, USub, parse, NodeVisitor, Expr, BinOp, UnaryOp, Name, Constant
)
from typing import List, Any, NoReturn
from operator import add, sub, mul, truediv, floordiv, mod, pow as opow, xor


class SafeEvaluator(NodeVisitor):
    """A safe evaluator that only allows basic math operations."""
    
    operators = {
        Add: add, Sub: sub,
        Mult: mul, Div: truediv,
        FloorDiv: floordiv, Mod: mod,
        Pow: opow, BitXor: xor
    }

    def __init__(self, variables):
        self.variables = variables

    def visit_BinOp(self, node: BinOp) -> Any:
        return self.operators[type(node.op)](self.visit(node.left), self.visit(node.right))

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


class Formula():
    def __init__(self, expression: str):
        """Initialize with a formula string and extract variable names dynamically."""
        self.expression = expression.upper()

        self.parsed_expr = parse(self.expression, mode="eval")

    def __call__(self, parsed_data: List[List[str]]) -> Any:
        """Evaluate the formula."""
        if not parsed_data or not parsed_data[0]:
            raise ValueError("Invalid parsed_data: must contain at least one non-empty list.")

        first_item = parsed_data[0]
        
        values = {
            chr(ord('A') + i): int(first_item[i], 16) 
            for i in range(len(first_item))
        }

        evaluator = SafeEvaluator(values)
        return evaluator.visit(self.parsed_expr.body)


class MultiFormula():
    def __init__(self, *expressions: str) -> None:
        """Initialize multiple Formula objects from a list of expressions."""
        self.formulas = [Formula(expr) for expr in expressions]

    def __call__(self, parsed_data: List[List[str]]) -> List[Any]:
        """Evaluate all stored formulas on the given parsed_data."""
        return [formula(parsed_data) for formula in self.formulas]