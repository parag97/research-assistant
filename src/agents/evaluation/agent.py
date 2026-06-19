from agents.base import BaseAgent

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
        research: str,
        reflection: str,
    ) -> EvaluationResult:

        return await self.runtime.llm.structured(
            prompt=evaluation_prompt(research, reflection),
            schema=EvaluationResult,
        )
