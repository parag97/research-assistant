from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    """Input model for CalculatorTool."""

    expression: str = Field(
        description=(
            "A mathematical expression to evaluate. "
            "Examples: '2 + 2', '10 * (3 + 4)', 'sqrt(16)'. "
            "Do not include assignment or variable definitions."
        )
    )
