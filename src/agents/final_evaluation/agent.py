from agents.base import BaseAgent

from core.models.artifact import (
    ResearchArtifact,
    ReflectionArtifact,
    FactCheckArtifact,
)
from core.runtime.agent_runtime import AgentRuntime
from core.models.final_evaluation import FinalEvaluationResult

from agents.final_evaluation.prompts import final_evaluation_prompt


class FinalEvaluationAgent(BaseAgent):

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.runtime = runtime

    async def run(
        self,
        research: ResearchArtifact,
        reflection: ReflectionArtifact,
        fact_check: FactCheckArtifact,
    ) -> FinalEvaluationResult:

        return await self.runtime.llm.structured(
            prompt=final_evaluation_prompt(
                research.content,
                reflection.content,
                fact_check.content,
            ),
            schema=FinalEvaluationResult,
        )
