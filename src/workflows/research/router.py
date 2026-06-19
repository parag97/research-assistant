from core.models.evaluation import (
    EvaluationDecision,
)

from workflows.research.state import (
    ResearchWorkflowState,
)


def evaluation_router(
    state: ResearchWorkflowState,
) -> str:
    """
    Routes workflow after evaluation.

    Decisions:
    - revise     -> go back to research
    - approve    -> continue to fact check

    Safety:
    - prevents infinite reflection loops
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

    print("============================\n")


    # Safety guard:
    # Never allow endless agent loops
    if revision_count >= 2:

        print(
            "Max revisions reached. Moving to fact check."
        )

        return "fact_check"


    if (
        evaluation.decision
        ==
        EvaluationDecision.REVISE
    ):

        print(
            "Research needs improvement. Sending back to Research Agent."
        )

        return "research"


    if (
        evaluation.decision
        ==
        EvaluationDecision.APPROVE
    ):

        print(
            "Research approved. Moving to Fact Check."
        )

        return "fact_check"


    raise ValueError(
        f"Unknown evaluation decision: {evaluation.decision}"
    )