from agents.base import BaseAgent

from core.models.artifact import ResearchArtifact, ReflectionArtifact
from core.models.evaluation import EvaluationResult
from core.runtime.agent_runtime import AgentRuntime

from agents.evaluation.prompts import evaluation_prompt


class EvaluationAgent(BaseAgent):

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.runtime = runtime

    async def run(
        self,
        research: ResearchArtifact,
        reflection: ReflectionArtifact,
    ) -> EvaluationResult:

        reflection_content = reflection.content if reflection else ""

        return await self.runtime.llm.structured(
            prompt=evaluation_prompt(research.content, reflection_content),
            schema=EvaluationResult,
        )
