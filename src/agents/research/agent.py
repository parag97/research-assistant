from agents.base import BaseAgent

from core.models.artifact import ResearchArtifact
from core.runtime.agent_runtime import AgentRuntime

from agents.research.prompts import research_prompt


class ResearchAgent(BaseAgent):

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.runtime = runtime

    async def run(
        self,
        query: str,
        feedback: str = "",
    ) -> ResearchArtifact:

        response = await self.runtime.llm.invoke(
            research_prompt(query, feedback)
        )

        return ResearchArtifact(
            content=response.content,
        )
