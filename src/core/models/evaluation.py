from enum import Enum

from pydantic import BaseModel, Field


class EvaluationDecision(str, Enum):
    APPROVE = "approve"
    REVISE = "revise"


class EvaluationResult(BaseModel):

    approved: bool

    score: float = Field(
        ge=0.0,
        le=1.0,
    )

    decision: EvaluationDecision

    feedback: str

    issues: list[str] = Field(
        default_factory=list
    )