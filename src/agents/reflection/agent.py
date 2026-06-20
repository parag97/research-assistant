from agents.base import BaseAgent

from core.models.artifact import ReflectionArtifact, ResearchArtifact
from core.runtime.agent_runtime import AgentRuntime

from agents.reflection.prompts import reflection_prompt


class ReflectionAgent(BaseAgent):

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.runtime = runtime

    async def run(
        self,
        research_artifact: ResearchArtifact,
    ) -> ReflectionArtifact:
        research_content = research_artifact.content
        response = await self.runtime.llm.invoke(
            reflection_prompt(research_content)
        )

        return ReflectionArtifact(
            content=response.content,
            confidence=0.8,
        )
