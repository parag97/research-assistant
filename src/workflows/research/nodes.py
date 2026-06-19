from core.runtime.agent_runtime import AgentRuntime

from core.models.artifact import (
    ReflectionArtifact,
    FactCheckArtifact,
)

from core.models.evaluation import (
    EvaluationResult,
)

from workflows.research.state import (
    ResearchWorkflowState,
)

from agents.research.agent import ResearchAgent
from agents.reflection.agent import ReflectionAgent
from agents.evaluation.agent import EvaluationAgent
from agents.fact_check.agent import FactCheckAgent


class ResearchNode:
    """
    Generates research artifact.
    """

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.agent = ResearchAgent(runtime)

    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):
        reflection = state.get("reflection")
        feedback = reflection.content if reflection else ""
        print(100*"+")
        print("+feedback: "+feedback)
        print(100*"+")
        response = await self.agent.run(
            query=state["query"],
            feedback=feedback,
        )

        return {
            "research": response,
            "revision_count": state.get("revision_count", 0) + 1,
        }


class ReflectionNode:
    """
    Critiques research quality.
    """

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.agent = ReflectionAgent(runtime)

    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):
        response = await self.agent.run(
            research_content=state["research"].content,
        )

        return {"reflection": response}


class FactCheckNode:
    """
    Validates final research.
    """

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.agent = FactCheckAgent(runtime)

    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):
        reflection = state.get("reflection")
        reflection_content = reflection.content if reflection else ""

        response = await self.agent.run(
            research=state["research"].content,
            reflection=reflection_content,
        )

        return {"fact_check": response}


class EvaluatorNode:
    """
    Decides whether research is ready or needs revision.
    """

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.agent = EvaluationAgent(runtime)

    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):
        reflection = state.get("reflection")
        reflection_content = reflection.content if reflection else ""

        result = await self.agent.run(
            research=state["research"].content,
            reflection=reflection_content,
        )

        return {"evaluation": result}
