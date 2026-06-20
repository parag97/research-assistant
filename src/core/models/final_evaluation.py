from pydantic import BaseModel, Field


class FinalEvaluationResult(BaseModel):

    score: float = Field(
        ge=0.0,
        le=1.0,
    )

    summary: str

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    ready_for_delivery: bool