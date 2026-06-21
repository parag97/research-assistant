from typing import TypedDict

from core.models.artifact import (
    FactCheckArtifact,
    ReflectionArtifact,
    ResearchArtifact,
)
from core.models.evaluation import EvaluationResult
from core.models.final_evaluation import FinalEvaluationResult


class ResearchWorkflowState(TypedDict, total=False):
    """
    Shared state passed between all nodes in the research workflow.

    All fields are optional (total=False) because LangGraph merges
    partial dicts returned by each node — no node sets every field.

    Fields
    ------
    query           : The original user question. Set at invocation, never mutated.
    research        : Latest research artifact produced by ResearchNode.
    reflection      : Critique of the research produced by ReflectionNode.
    evaluation      : Structured approval/revision decision from EvaluatorNode.
    fact_check      : Fact-checking report produced by FactCheckNode.
    final_evaluation: Final quality assessment produced by FinalEvaluationNode.
    revision_count  : Number of times ResearchNode has run. Used by the router
                      to enforce the maximum-revision safety cap.
    errors          : Accumulated non-fatal error messages from failed nodes.
                      Nodes that catch exceptions append here rather than raising,
                      allowing the workflow to continue in a degraded state.
    """

    query: str

    research: ResearchArtifact

    reflection: ReflectionArtifact

    evaluation: EvaluationResult

    fact_check: FactCheckArtifact

    final_evaluation: FinalEvaluationResult

    revision_count: int

    errors: list[str]
