from enum import Enum

from pydantic import BaseModel, Field


class EvaluationDecision(str, Enum):
    """
    Decision produced by the EvaluationAgent after reviewing research quality.

    APPROVE : Research is good enough to proceed to fact-checking.
    REVISE  : Research needs another pass through the research→reflection loop.
    """

    APPROVE = "approve"
    REVISE = "revise"


class EvaluationResult(BaseModel):
    """
    Structured output returned by the EvaluationAgent.

    Used by EvaluationRouter to decide whether to loop back to ResearchNode
    or proceed to FactCheckNode.

    Fields
    ------
    approved : True if the research is approved for the next stage.
    score    : Quality score between 0.0 and 1.0.
    decision : Explicit APPROVE / REVISE routing signal.
    feedback : Human-readable justification for the decision.
    issues   : Specific problems identified (populated on REVISE).
    """

    approved: bool
    score: float = Field(ge=0.0, le=1.0)
    decision: EvaluationDecision
    feedback: str
    issues: list[str] = Field(default_factory=list)
