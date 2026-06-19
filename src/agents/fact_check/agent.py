from agents.base import BaseAgent

from core.models.artifact import FactCheckArtifact
from core.runtime.agent_runtime import AgentRuntime

from agents.fact_check.prompts import fact_check_prompt


class FactCheckAgent(BaseAgent):

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.runtime = runtime

    async def run(
        self,
        research: str,
        reflection: str,
    ) -> FactCheckArtifact:

        response = await self.runtime.llm.invoke(
            fact_check_prompt(research, reflection)
        )

        return FactCheckArtifact(
            content=response.content,
            confidence=0.9,
        )
