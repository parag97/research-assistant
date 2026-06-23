import logging

from core.observability.decorators import trace_node
from core.models.artifact import ReflectionArtifact, FactCheckArtifact

from workflows.research.state import ResearchWorkflowState

from agents.research.agent import ResearchAgent
from agents.reflection.agent import ReflectionAgent
from agents.evaluation.agent import EvaluationAgent
from agents.fact_check.agent import FactCheckAgent
from agents.final_evaluation.agent import FinalEvaluationAgent

logger = logging.getLogger(__name__)


class ResearchNode:
    """
    Runs the ResearchAgent to produce or revise a ResearchArtifact.

    On subsequent passes the reflection content is forwarded as feedback
    so the agent can improve on its previous attempt.
    Increments revision_count on every execution.
    """

    def __init__(self, agent: ResearchAgent) -> None:
        self.agent = agent

    @trace_node("ResearchNode")
    async def __call__(
        self,
        state: ResearchWorkflowState,
    ) -> dict:

        # Carry forward any existing errors from earlier nodes
        errors: list[str] = list(state.get("errors") or [])

        # Extract feedback from the previous reflection, if any
        reflection = state.get("reflection")
        feedback = reflection.content if reflection else ""

        try:
            response = await self.agent.run(
                query=state["query"],
                feedback=feedback,
            )
        except Exception as exc:
            error_msg = f"ResearchNode failed: {exc}"
            logger.error(error_msg)
            errors.append(error_msg)
            # Re-raise — without a research artifact the workflow cannot continue
            raise

        return {
            "research": response,
            "revision_count": state.get("revision_count", 0) + 1,
            "errors": errors,
        }


class ReflectionNode:
    """
    Runs the ReflectionAgent to critique the current ResearchArtifact.

    On failure a minimal placeholder reflection is injected so the
    workflow can still proceed to evaluation rather than hard-crashing.
    """

    def __init__(self, agent: ReflectionAgent) -> None:
        self.agent = agent

    @trace_node("ReflectionNode")
    async def __call__(
        self,
        state: ResearchWorkflowState,
    ) -> dict:

        errors: list[str] = list(state.get("errors") or [])

        try:
            response = await self.agent.run(
                research_artifact=state["research"],
            )
            return {
                "reflection": response,
                "errors": errors,
            }

        except Exception as exc:
            error_msg = f"ReflectionNode failed: {exc}"
            logger.error(error_msg)
            errors.append(error_msg)

            # Degrade gracefully: inject a stub so evaluation can still run
            stub = ReflectionArtifact(
                content="Reflection unavailable due to an error.",
                confidence=0.0,
            )
            return {
                "reflection": stub,
                "errors": errors,
            }


class EvaluatorNode:
    """
    Runs the EvaluationAgent to decide whether the research is ready
    or needs another revision pass.

    On failure the router falls back to the revision cap, so the
    workflow still terminates rather than looping indefinitely.
    """

    def __init__(self, agent: EvaluationAgent) -> None:
        self.agent = agent

    @trace_node("EvaluatorNode")
    async def __call__(
        self,
        state: ResearchWorkflowState,
    ) -> dict:

        errors: list[str] = list(state.get("errors") or [])

        try:
            result = await self.agent.run(
                research=state["research"],
                reflection=state.get("reflection"),
            )
            return {
                "evaluation": result,
                "errors": errors,
            }

        except Exception as exc:
            error_msg = f"EvaluatorNode failed: {exc}"
            logger.error(error_msg)
            errors.append(error_msg)

            # Leave evaluation as None — the router handles this by
            # forcing a transition to fact_check via the revision cap.
            return {"errors": errors}


class FactCheckNode:
    """
    Runs the FactCheckAgent to validate the final research artifact.

    On failure a minimal stub is injected so the workflow can still
    reach FinalEvaluationNode and produce a result.
    """

    def __init__(self, agent: FactCheckAgent) -> None:
        self.agent = agent

    @trace_node("FactCheckNode")
    async def __call__(
        self,
        state: ResearchWorkflowState,
    ) -> dict:

        errors: list[str] = list(state.get("errors") or [])

        try:
            response = await self.agent.run(
                research=state["research"],
                reflection=state.get("reflection"),
            )
            return {
                "fact_check": response,
                "errors": errors,
            }

        except Exception as exc:
            error_msg = f"FactCheckNode failed: {exc}"
            logger.error(error_msg)
            errors.append(error_msg)

            # Degrade gracefully: inject a stub so final evaluation can run
            stub = FactCheckArtifact(
                content="Fact-check unavailable due to an error.",
                confidence=0.0,
            )
            return {
                "fact_check": stub,
                "errors": errors,
            }


class FinalEvaluationNode:
    """
    Runs the FinalEvaluationAgent to score the completed research report.

    This is the last node before END. On failure an error is recorded
    and the exception is re-raised so the caller receives a clear signal
    that the final assessment could not be completed.
    """

    def __init__(self, agent: FinalEvaluationAgent) -> None:
        self.agent = agent

    @trace_node("FinalEvaluationNode")
    async def __call__(
        self,
        state: ResearchWorkflowState,
    ) -> dict:

        errors: list[str] = list(state.get("errors") or [])

        try:
            response = await self.agent.run(
                research=state["research"],
                reflection=state["reflection"],
                fact_check=state["fact_check"],
            )
            return {
                "final_evaluation": response,
                "errors": errors,
            }

        except Exception as exc:
            error_msg = f"FinalEvaluationNode failed: {exc}"
            logger.error(error_msg)
            errors.append(error_msg)
            # Re-raise — the caller needs to know the final report is incomplete
            raise
