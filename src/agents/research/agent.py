import asyncio
import json
import logging

from core.models.artifact import ResearchArtifact
from core.runtime.agent_runtime import AgentRuntime
from tools.models import ToolPlan

from agents.research.prompts import SYNTHESIS_PROMPT, TOOL_PLANNING_PROMPT

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    Produces a ResearchArtifact for a given query.

    Pipeline
    --------
    1. Plan     — ask the LLM which tools to call and with what arguments.
    2. Execute  — run all planned tool calls concurrently.
    3. Synthesize — write the research using the tool results.

    All tuneable parameters are injected by the Container as plain values.
    This class never reads config itself.
    """

    def __init__(
        self,
        runtime: AgentRuntime,
        max_retries: int,
        structured_retries: int,
        retry_backoff: float,
        confidence: float,
    ) -> None:
        self.runtime = runtime
        self._max_retries = max_retries
        self._structured_retries = structured_retries
        self._retry_backoff = retry_backoff
        self._confidence = confidence

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _plan_tools(
        self,
        query: str,
        feedback: str | None = None,
    ) -> ToolPlan:
        """
        Ask the LLM to produce a structured ToolPlan for the query.

        Uses structured_retries (higher cap) because JSON schema compliance
        is less reliable on small models. Falls back to an empty plan when
        all retries are exhausted so synthesis can still proceed.
        """

        prompt = TOOL_PLANNING_PROMPT.format(
            query=query,
            feedback=feedback or "No previous feedback.",
            tools=json.dumps(self.runtime.tools.descriptions(), indent=2),
        )

        last_exc: Exception | None = None

        for attempt in range(1, self._structured_retries + 1):
            try:
                return await self.runtime.llm.structured(
                    prompt=prompt,
                    schema=ToolPlan,
                )
            except Exception as exc:
                last_exc = exc
                logger.warning(
                    "Tool planning attempt %d/%d failed: %s",
                    attempt, self._structured_retries, exc,
                )
                if attempt < self._structured_retries:
                    await asyncio.sleep(self._retry_backoff * attempt)

        logger.error(
            "Tool planning failed after %d attempts — proceeding without tools. "
            "Last error: %s",
            self._structured_retries, last_exc,
        )
        return ToolPlan(tool_calls=[])

    async def _execute_tools(self, plan: ToolPlan) -> list:
        """
        Execute all tool calls from the plan concurrently.

        Individual failures are caught and returned as error entries so
        the synthesizer has context about what was unavailable.
        """

        if not plan.tool_calls:
            return []

        async def _run_one(tool_call):
            try:
                tool = self.runtime.tools.get(tool_call.tool_name)
                return await tool.execute(**tool_call.arguments)
            except Exception as exc:
                logger.warning("Tool '%s' failed: %s", tool_call.tool_name, exc)
                return {"tool": tool_call.tool_name, "error": str(exc)}

        return await asyncio.gather(*[_run_one(tc) for tc in plan.tool_calls])

    async def _synthesize(
        self,
        query: str,
        feedback: str | None,
        tool_results: list,
    ):
        """
        Ask the LLM to write research from the collected tool results.
        Retries with exponential backoff on transient failures.
        """

        prompt = SYNTHESIS_PROMPT.format(
            query=query,
            feedback=feedback or "No previous feedback.",
            tool_results=json.dumps(tool_results, indent=2),
        )

        last_exc: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                return await self.runtime.llm.invoke(prompt)
            except Exception as exc:
                last_exc = exc
                logger.warning(
                    "Synthesis attempt %d/%d failed: %s",
                    attempt, self._max_retries, exc,
                )
                if attempt < self._max_retries:
                    await asyncio.sleep(self._retry_backoff * attempt)

        raise RuntimeError(
            f"Synthesis failed after {self._max_retries} attempts."
        ) from last_exc

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    async def run(
        self,
        query: str,
        feedback: str | None = None,
    ) -> ResearchArtifact:
        """
        Run the full research pipeline and return a ResearchArtifact.

        Parameters
        ----------
        query    : The research question.
        feedback : Optional critique from a previous reflection pass.
        """

        # Step 1: decide which tools to call
        plan = await self._plan_tools(query=query, feedback=feedback)
        logger.debug("Tool plan: %s", plan.model_dump_json(indent=2))

        # Step 2: execute all tool calls concurrently
        tool_results = await self._execute_tools(plan)
        logger.debug("Tool results: %s", json.dumps(tool_results, indent=2))

        # Step 3: synthesise research from tool outputs
        response = await self._synthesize(
            query=query,
            feedback=feedback,
            tool_results=tool_results,
        )

        return ResearchArtifact(
            content=response.content,
            confidence=self._confidence,
        )
