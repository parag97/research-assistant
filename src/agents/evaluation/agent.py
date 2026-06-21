import asyncio
import logging

from agents.base import BaseAgent
from core.models.artifact import ReflectionArtifact, ResearchArtifact
from core.models.evaluation import EvaluationResult
from core.runtime.agent_runtime import AgentRuntime

from agents.evaluation.prompts import evaluation_prompt

logger = logging.getLogger(__name__)


class EvaluationAgent(BaseAgent):
    """
    Evaluates the quality of a research + reflection pair.

    Returns a structured EvaluationResult with an approval/revision
    decision, a score, and feedback for the next research iteration.

    Uses structured output (JSON schema) — retried aggressively since
    small models occasionally produce malformed responses.
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
        reflection: ReflectionArtifact | None,
    ) -> EvaluationResult:
        """
        Evaluate research quality and return an EvaluationResult.

        Parameters
        ----------
        research   : The research artifact to evaluate.
        reflection : The corresponding reflection (may be None on first pass).
        """

        reflection_content = reflection.content if reflection else ""
        prompt = evaluation_prompt(research.content, reflection_content)
        last_exc: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                return await self.runtime.llm.structured(
                    prompt=prompt,
                    schema=EvaluationResult,
                )
            except Exception as exc:
                last_exc = exc
                logger.warning(
                    "Evaluation attempt %d/%d failed: %s",
                    attempt, self._max_retries, exc,
                )
                if attempt < self._max_retries:
                    await asyncio.sleep(self._retry_backoff * attempt)

        raise RuntimeError(
            f"Evaluation failed after {self._max_retries} attempts."
        ) from last_exc
