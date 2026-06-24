import asyncio
import logging

from agents.base import BaseAgent
from core.models.artifact import ReflectionArtifact, ResearchArtifact
from core.runtime.agent_runtime import AgentRuntime

from agents.reflection.prompts import reflection_prompt

logger = logging.getLogger(__name__)


class ReflectionAgent(BaseAgent):
    """
    Critiques a ResearchArtifact and returns a ReflectionArtifact.

    Looks for missing information, weak reasoning, and unsupported claims.
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
        research_artifact: ResearchArtifact,
    ) -> ReflectionArtifact:
        """
        Critique the research and return a ReflectionArtifact.

        Parameters
        ----------
        research_artifact : The research artifact to critique.
        """

        with self.runtime.tracer.span("ReflectionAgent") as span:
            span.set_attribute("agnent.name", "reflection")
            prompt = reflection_prompt(research_artifact.content)
            last_exc: Exception | None = None

            for attempt in range(1, self._max_retries + 1):
                try:
                    with self.runtime.tracer.span("Reflection"):
                        response = await self.runtime.llm.invoke(prompt)
                    return ReflectionArtifact(
                        content=response.content,
                        confidence=self._confidence,
                    )
                except Exception as exc:
                    last_exc = exc
                    logger.warning(
                        "Reflection attempt %d/%d failed: %s",
                        attempt, self._max_retries, exc,
                    )
                    if attempt < self._max_retries:
                        await asyncio.sleep(self._retry_backoff * attempt)

            raise RuntimeError(
                f"Reflection failed after {self._max_retries} attempts."
            ) from last_exc
