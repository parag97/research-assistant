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

        try:
            request = CalculatorInput(
                **kwargs
            )

            result = eval(
                request.expression,
                {"__builtins__": {}},
                {},
            )

        except Exception as e:
            return {
                "expression":
                    "",
                "result":
                    str(e),
            }


        return {
            "expression":
                request.expression,
            "result":
                result,
        }