from core.llm.base import LLMProvider

from core.models.artifact import (
    ResearchArtifact,
    ReflectionArtifact,
    FactCheckArtifact,
)

from core.models.evaluation import (
    EvaluationResult,
)

from workflows.research.state import (
    ResearchWorkflowState,
)


class ResearchNode:
    """
    Generates research artifact.
    """

    def __init__(
        self,
        llm: LLMProvider,
    ):
        self.llm = llm


    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):

        response = await self.llm.invoke(
            f"""
            You are a research agent.

            Research this topic:

            {state["query"]}

            Produce:
            - Important facts
            - Context
            - Explanations
            - Key points
            """
        )

        current_revision = state.get(
            "revision_count",
            0,
        )

        return {
            "research": ResearchArtifact(
                content=response.content,
                confidence=0.8,
            ),

            "revision_count":
                current_revision + 1,
        }


class ReflectionNode:
    """
    Critiques research quality.
    """

    def __init__(
        self,
        llm: LLMProvider,
    ):
        self.llm = llm


    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):

        response = await self.llm.invoke(
            f"""
            You are a reflection agent.

            Critically review the research.

            Find:
            - Missing information
            - Weak reasoning
            - Unsupported claims
            - Possible hallucinations


            Research:

            {state["research"].content}
            """
        )

        return {
            "reflection":
                ReflectionArtifact(
                    content=response.content,
                    confidence=0.8,
                )
        }


class FactCheckNode:
    """
    Validates final research.
    """

    def __init__(
        self,
        llm: LLMProvider,
    ):
        self.llm = llm


    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):

        response = await self.llm.invoke(
            f"""
            You are a fact checking agent.

            Verify this research.

            Check:
            - Accuracy
            - Unsupported statements
            - Contradictions


            Research:

            {state["research"].content}


            Reflection:

            {state["reflection"].content}
            """
        )

        return {
            "fact_check":
                FactCheckArtifact(
                    content=response.content,
                    confidence=0.9,
                )
        }




class EvaluatorNode:

    def __init__(
        self,
        llm,
    ):
        self.llm = llm


    async def __call__(
        self,
        state: ResearchWorkflowState,
    ):

        result = await self.llm.structured(
            prompt=f"""
            Evaluate this research.

            Decide if it is ready.

            Research:
            {state["research"].content}


            Reflection:
            {state["reflection"].content}
            """,

            schema=EvaluationResult,
        )


        return {
            "evaluation": result
        }