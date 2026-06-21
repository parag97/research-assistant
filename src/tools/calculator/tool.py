import logging

from tools.base import BaseTool
from tools.calculator.models import CalculatorInput

logger = logging.getLogger(__name__)


class CalculatorTool(BaseTool):
    """
    Evaluates a mathematical expression and returns the result.

    Uses Python's eval() with an empty builtins dict to prevent arbitrary
    code execution. Only numeric operations and standard operators are safe
    in this sandbox — no function calls or imports are allowed.
    """

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return (
            "Evaluate a mathematical expression and return the numeric result. "
            "Supports standard arithmetic operators: +, -, *, /, **, %."
        )

    @property
    def input_model(self):
        return CalculatorInput

    async def execute(self, **kwargs) -> dict:

        request = CalculatorInput(**kwargs)

        try:
            # Restricted eval: empty builtins prevents imports and built-in
            # function access, limiting execution to pure arithmetic.
            result = eval(
                request.expression,
                {"__builtins__": {}},
                {},
            )
            return {
                "expression": request.expression,
                "result": result,
            }

        except Exception as exc:
            logger.warning(
                "CalculatorTool failed for expression '%s': %s",
                request.expression,
                exc,
            )
            return {
                "expression": request.expression,
                "result": f"Error: {exc}",
            }
