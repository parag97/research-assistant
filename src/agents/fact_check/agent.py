import asyncio
import logging

from agents.base import BaseAgent
from core.models.artifact import (
    FactCheckArtifact,
    ReflectionArtifact,
    ResearchArtifact,
)
from core.runtime.agent_runtime import AgentRuntime

from agents.fact_check.prompts import fact_check_prompt

logger = logging.getLogger(__name__)


class FactCheckAgent(BaseAgent):
    """
    Validates a ResearchArtifact against its ReflectionArtifact.

    Checks for factual inaccuracies, unsupported statements, and
    internal contradictions.
    All tuneable parameters are injected by the Container as plain values.
    """

    def __init__(
        self,
        runtime: AgentRuntime,
        max_retries: int,
        retry_backoff: float,
        confidence: float,
    ) -> None:
        self.runtime = runtime
        self._max_retries = max_retries
        self._retry_backoff = retry_backoff
        self._confidence = confidence

    async def run(
        self,
        research: ResearchArtifact,
        reflection: ReflectionArtifact | None,
    ) -> FactCheckArtifact:
        """
        Fact-check the research artifact and return a FactCheckArtifact.

        Parameters
        ----------
        research   : The research artifact to validate.
        reflection : The reflection critique to cross-reference (may be None).
        """

        reflection_content = reflection.content if reflection else ""
        prompt = fact_check_prompt(research.content, reflection_content)
        last_exc: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                response = await self.runtime.llm.invoke(prompt)
                return FactCheckArtifact(
                    content=response.content,
                    confidence=self._confidence,
                )
            except Exception as exc:
                last_exc = exc
                logger.warning(
                    "Fact-check attempt %d/%d failed: %s",
                    attempt, self._max_retries, exc,
                )
                if attempt < self._max_retries:
                    await asyncio.sleep(self._retry_backoff * attempt)

        raise RuntimeError(
            f"Fact-check failed after {self._max_retries} attempts."
        ) from last_exc
