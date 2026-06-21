from pydantic import BaseModel, Field


class FinalEvaluationResult(BaseModel):
    """
    Structured output returned by the FinalEvaluationAgent.

    Produced once at the end of the workflow after fact-checking is complete.
    Assesses the overall quality of the research deliverable as it would
    appear to an end user.

    Fields
    ------
    score             : Overall quality score between 0.0 and 1.0.
    summary           : Concise one-paragraph assessment.
    strengths         : Notable positive aspects of the research.
    weaknesses        : Remaining gaps or issues in the research.
    ready_for_delivery: True if the report is suitable to show to an end user.
    """

    score: float = Field(ge=0.0, le=1.0)
    summary: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    ready_for_delivery: bool
