import logging

from langgraph.graph import END, START, StateGraph

from core.workflow.base_workflow import BaseWorkflow

from agents.research.agent import ResearchAgent
from agents.reflection.agent import ReflectionAgent
from agents.evaluation.agent import EvaluationAgent
from agents.fact_check.agent import FactCheckAgent
from agents.final_evaluation.agent import FinalEvaluationAgent


from workflows.research.nodes import (
    EvaluatorNode,
    FactCheckNode,
    FinalEvaluationNode,
    ReflectionNode,
    ResearchNode,
)
from workflows.research.router import EvaluationRouter
from workflows.research.state import ResearchWorkflowState

logger = logging.getLogger(__name__)


class ResearchWorkflow(BaseWorkflow):
    """
    Multi-agent research workflow built on LangGraph.

    Graph topology
    --------------
    START
      └─> research ──> reflection ──> evaluation
                           ▲               │
                           │    (REVISE)   │
                           └───────────────┘
                                           │ (APPROVE or cap reached)
                                           ▼
                                      fact_check
                                           │
                                           ▼
                                    final_evaluation
                                           │
                                           ▼
                                          END

    Nodes
    -----
    research         : Generates / revises the research artifact.
    reflection       : Critiques the research for gaps and weak reasoning.
    evaluation       : Approves or requests revision (structured output).
    fact_check       : Validates accuracy of the approved research.
    final_evaluation : Scores the completed deliverable for the end user.

    Retry / error handling
    ----------------------
    Each agent retries its LLM calls internally.
    Nodes catch agent errors and either degrade gracefully (inject stubs)
    or re-raise when the workflow cannot meaningfully continue.
    The router handles a missing evaluation result without crashing.
    """

    def __init__(
        self, 
        research_agent: ResearchAgent,
        reflection_agent: ReflectionAgent,
        evaluation_agent: EvaluationAgent,
        fact_check_agent: FactCheckAgent,
        final_evaluation_agent: FinalEvaluationAgent,
        max_revisions: int
        ) -> None:

        self._router = EvaluationRouter(max_revisions=max_revisions)
        self.research_agent = research_agent
        self.reflection_agent = reflection_agent
        self.evaluation_agent = evaluation_agent
        self.fact_check_agent = fact_check_agent
        self.final_evaluation_agent = final_evaluation_agent






    def build(self):
        """Compile and return the LangGraph StateGraph."""

        graph = StateGraph(ResearchWorkflowState)

        # ------------------------------------------------------------------
        # Register nodes
        # ------------------------------------------------------------------

        graph.add_node(
            "research",
            ResearchNode(self.research_agent),
        )

        graph.add_node(
            "reflection",
            ReflectionNode(self.reflection_agent),
        )

        graph.add_node(
            "evaluation",
            EvaluatorNode(self.evaluation_agent),
        )

        graph.add_node(
            "fact_check",
            FactCheckNode(self.fact_check_agent),
        )

        graph.add_node(
            "final_evaluation",
            FinalEvaluationNode(self.final_evaluation_agent),
        )

        # ------------------------------------------------------------------
        # Main flow: research -> reflection -> evaluation
        # ------------------------------------------------------------------

        graph.add_edge(START, "research")
        graph.add_edge("research", "reflection")
        graph.add_edge("reflection", "evaluation")

        # ------------------------------------------------------------------
        # Revision loop: evaluation routes back to research or forward
        # ------------------------------------------------------------------

        graph.add_conditional_edges(
            "evaluation",
            self._router,
            {
                "research": "research",
                "fact_check": "fact_check",
            },
        )

        # ------------------------------------------------------------------
        # Final validation: fact_check -> final_evaluation -> END
        # ------------------------------------------------------------------

        graph.add_edge("fact_check", "final_evaluation")
        graph.add_edge("final_evaluation", END)

        logger.info("ResearchWorkflow graph compiled.")

        return graph.compile()