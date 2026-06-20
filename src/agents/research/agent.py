import asyncio
import json

from core.models.artifact import ResearchArtifact
from core.runtime.agent_runtime import AgentRuntime

from tools.models import ToolPlan

from agents.research.prompts import (
    TOOL_PLANNING_PROMPT,
    SYNTHESIS_PROMPT,
)


class ResearchAgent:

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.runtime = runtime

    async def _plan_tools(
        self,
        query: str,
        feedback: str | None = None,
    ) -> ToolPlan:

        available_tools = (
            self.runtime.tools.descriptions()
        )
        prompt = TOOL_PLANNING_PROMPT.format(
            query=query,
            feedback=feedback or "No feedback available.",
            tools=json.dumps(
                available_tools,
                indent=2,
            ),
        )

        return await (
            self.runtime.llm.structured(
                prompt=prompt,
                schema=ToolPlan,
            )
        )

    async def _execute_tools(
        self,
        plan: ToolPlan,
    ) -> list:

        if not plan.tool_calls:
            return []

        tasks = []

        for tool_call in plan.tool_calls:

            tool = (
                self.runtime
                .tools
                .get(
                    tool_call.tool_name
                )
            )

            tasks.append(
                tool.execute(
                    **tool_call.arguments
                )
            )

        return await asyncio.gather(
            *tasks
        )

    async def _synthesize(
        self,
        query: str,
        feedback: str | None,
        tool_results: list,
    ):

        prompt = SYNTHESIS_PROMPT.format(
            query=query,
            feedback=feedback or "No feedback available.",
            tool_results=json.dumps(
                tool_results,
                indent=2,
            ),
        )

        return await (
            self.runtime.llm.invoke(
                prompt
            )
        )

    async def run(
        self,
        query: str,
        feedback: str | None = None,
    ) -> ResearchArtifact:

        plan = await self._plan_tools(
            query=query,
            feedback=feedback,
        )

        print("\n=== TOOL PLAN ===")
        print(
            plan.model_dump_json(
                indent=2
            )
        )

        tool_results = await (
            self._execute_tools(
                plan
            )
        )

        print("\n=== TOOL RESULTS ===")
        print(
            json.dumps(
                tool_results,
                indent=2,
            )
        )

        response = await (
            self._synthesize(
                query=query,
                feedback=feedback,
                tool_results=tool_results,
            )
        )

        return ResearchArtifact(
            content=response.content,
            confidence=0.8,
        )