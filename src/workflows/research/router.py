from core.models.evaluation import (
    EvaluationDecision,
)

from workflows.research.state import (
    ResearchWorkflowState,
)


MAX_REVISIONS = 2


def evaluation_router(
    state: ResearchWorkflowState,
) -> str:
    """
    Routes workflow after evaluation.

    Decisions:
    - revise     -> go back to research
    - approve    -> continue to fact check

    Safety:
    - prevents infinite revision loops
    """

    revision_count = state.get(
        "revision_count",
        0,
    )

    evaluation = state.get(
        "evaluation",
    )

    if evaluation is None:
        raise ValueError(
            "Evaluation missing from workflow state"
        )

    print("\n========== ROUTER ==========")

    print(
        f"Revision Count: {revision_count}"
    )

    print(
        f"Decision: {evaluation.decision}"
    )

    print(
        f"Score: {evaluation.score}"
    )

    print(
        f"Approved: {evaluation.approved}"
    )

    print("============================\n")

    #
    # Safety Guard
    #

    if revision_count >= MAX_REVISIONS:

        print(
            "Maximum revisions reached. "
            "Proceeding to Fact Check."
        )

        return "fact_check"

    #
    # Revision Required
    #

    if (
        evaluation.decision
        ==
        EvaluationDecision.REVISE
    ):

        print(
            "Research requires revision."
        )

        return "research"

    #
    # Approved
    #

    if (
        evaluation.decision
        ==
        EvaluationDecision.APPROVE
    ):

        print(
            "Research approved."
        )

        return "fact_check"

    raise ValueError(
        f"Unknown evaluation decision: "
        f"{evaluation.decision}"
    )