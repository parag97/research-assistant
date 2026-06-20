from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    expression: str = Field(
        description="Mathematical expression to evaluate"
    )