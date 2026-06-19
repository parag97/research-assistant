from typing import TypedDict

from core.models.artifact import (
    ResearchArtifact,
    ReflectionArtifact,
    FactCheckArtifact,
)

from core.models.evaluation import (
    EvaluationResult,
)


class ResearchWorkflowState(
    TypedDict,
    total=False,
):
    query: str

    research: ResearchArtifact

    reflection: ReflectionArtifact

    evaluation: EvaluationResult

    fact_check: FactCheckArtifact

    revision_count: int