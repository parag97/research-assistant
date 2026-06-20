from tools.base import BaseTool
from tools.calculator.models import CalculatorInput


class CalculatorTool(BaseTool):

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return (
            "Evaluate mathematical expressions"
        )

    @property
    def input_model(self):
        return CalculatorInput

    async def execute(
        self,
        **kwargs,
    ):

        request = CalculatorInput(
            **kwargs
        )

        result = eval(
            request.expression,
            {"__builtins__": {}},
            {},
        )

        return {
            "expression":
                request.expression,
            "result":
                result,
        }