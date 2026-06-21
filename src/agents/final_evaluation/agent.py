import asyncio
import logging

from agents.base import BaseAgent
from core.models.artifact import (
    FactCheckArtifact,
    ReflectionArtifact,
    ResearchArtifact,
)
from core.models.final_evaluation import FinalEvaluationResult
from core.runtime.agent_runtime import AgentRuntime

from agents.final_evaluation.prompts import final_evaluation_prompt

logger = logging.getLogger(__name__)


class FinalEvaluationAgent(BaseAgent):
    """
    Produces the final quality assessment for the completed research report.

    Unlike EvaluationAgent (which decides approve/revise mid-workflow),
    this agent runs once at the end after fact-checking and scores the
    overall deliverable quality for the end user.

    Uses structured output — retried aggressively to handle small-model
    JSON formatting issues.
    All tuneable parameters are injected by the Container as plain values.
    """

    def __init__(
        self,
        runtime: AgentRuntime,
        max_retries: int,
        retry_backoff: float,
    ) -> None:
        self.runtime = runtime
        self._max_retries = max_retries
        self._retry_backoff = retry_backoff

    async def run(
        self,
        research: ResearchArtifact,
        reflection: ReflectionArtifact,
        fact_check: FactCheckArtifact,
    ) -> FinalEvaluationResult:
        """
        Assess the final research deliverable and return a FinalEvaluationResult.

        Parameters
        ----------
        research   : The final research artifact.
        reflection : The reflection critique that was applied.
        fact_check : The fact-checking report.
        """

        prompt = final_evaluation_prompt(
            research.content,
            reflection.content,
            fact_check.content,
        )

        last_exc: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                return await self.runtime.llm.structured(
                    prompt=prompt,
                    schema=FinalEvaluationResult,
                )
            except Exception as exc:
                last_exc = exc
                logger.warning(
                    "Final evaluation attempt %d/%d failed: %s",
                    attempt, self._max_retries, exc,
                )
                if attempt < self._max_retries:
                    await asyncio.sleep(self._retry_backoff * attempt)

        raise RuntimeError(
            f"Final evaluation failed after {self._max_retries} attempts."
        ) from last_exc
