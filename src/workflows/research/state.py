from typing import TypedDict

from core.models.artifact import (
    ResearchArtifact,
    ReflectionArtifact,
    FactCheckArtifact,
    
)

from core.models.evaluation import (
    EvaluationResult,
    
)

from core.models.final_evaluation import (
    FinalEvaluationResult,
    
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

    final_evaluation: FinalEvaluationResult

    revision_count: int