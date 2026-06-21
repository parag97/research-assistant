import logging

from core.models.evaluation import EvaluationDecision
from workflows.research.state import ResearchWorkflowState

logger = logging.getLogger(__name__)


class EvaluationRouter:
    """
    Conditional edge callable for the evaluation node in the research workflow.

    Determines whether the workflow loops back to ResearchNode for another
    revision pass, or continues forward to FactCheckNode.

    max_revisions is injected by the Container as a plain int — this class
    never reads config itself.

    Decision logic
    --------------
    1. revision_count >= max_revisions  -> fact_check  (safety cap)
    2. evaluation is None               -> fact_check  (node failed, degrade)
    3. decision == REVISE               -> research    (revision loop)
    4. decision == APPROVE              -> fact_check  (happy path)
    """

    def __init__(self, max_revisions: int) -> None:
        self._max_revisions = max_revisions

    def __call__(self, state: ResearchWorkflowState) -> str:

        revision_count = state.get("revision_count", 0)
        evaluation = state.get("evaluation")

        logger.info(
            "Router — revision_count=%d / max=%d, decision=%s, score=%s",
            revision_count,
            self._max_revisions,
            evaluation.decision if evaluation else "N/A",
            f"{evaluation.score:.2f}" if evaluation else "N/A",
        )

        # Safety cap: never loop more than max_revisions times
        if revision_count >= self._max_revisions:
            logger.info(
                "Maximum revisions (%d) reached. Proceeding to fact-check.",
                self._max_revisions,
            )
            return "fact_check"

        # Graceful degradation: evaluation node failed
        if evaluation is None:
            logger.warning(
                "Evaluation result missing (node may have failed). "
                "Proceeding to fact-check."
            )
            return "fact_check"

        # Normal routing
        if evaluation.decision == EvaluationDecision.REVISE:
            logger.info("Decision: REVISE. Sending back to research.")
            return "research"

        if evaluation.decision == EvaluationDecision.APPROVE:
            logger.info("Decision: APPROVE. Proceeding to fact-check.")
            return "fact_check"

        raise ValueError(f"Unknown evaluation decision: {evaluation.decision}")
