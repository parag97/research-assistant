from workflows.research.state import (
    ResearchWorkflowState,
)

from agents.research.agent import ResearchAgent
from agents.reflection.agent import ReflectionAgent
from agents.evaluation.agent import EvaluationAgent
from agents.fact_check.agent import FactCheckAgent
from agents.final_evaluation.agent import FinalEvaluationAgent


class ResearchNode:
    """
    Generates research artifact.
    """

    def __init__(
        self,
        agent: ResearchAgent,
    ):
        self.agent = agent

    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):
        reflection = state.get("reflection")
        feedback = reflection.content if reflection else ""
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
        agent: ReflectionAgent,
    ):
        self.agent = agent

    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):
        response = await self.agent.run(
            research_artifact = state["research"],
        )

        return {"reflection": response}


class FactCheckNode:
    """
    Validates final research.
    """

    def __init__(
        self,
        agent: FactCheckAgent,
    ):
        self.agent = agent

    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):
        reflection = state.get("reflection")
        response = await self.agent.run(
            research=state["research"],
            reflection = reflection,
        )

        return {"fact_check": response}


class EvaluatorNode:
    """
    Decides whether research is ready or needs revision.
    """

    def __init__(
        self,
        agent :EvaluationAgent,
    ):
        self.agent = agent

    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):
        reflection = state.get("reflection")

        result = await self.agent.run(
            research=state["research"],
            reflection=reflection,
        )

        return {"evaluation": result}


class FinalEvaluationNode:
    
    """
    Makes final decision on whether to end workflow.
    """

    def __init__(
        self,
        agent: FinalEvaluationAgent,
    ):
        self.agent = agent

    async def __call__(
        self,
        state: ResearchWorkflowState,    
    ):
        response = await self.agent.run(
            research=state["research"],
            reflection=state["reflection"],
            fact_check=state["fact_check"],
        )
        return {"final_evaluation": response}

