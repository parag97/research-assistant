from langgraph.graph import (
    START,
    END,
    StateGraph,
)

from core.dependencies.container import Container
from core.workflow.base_workflow import BaseWorkflow

from workflows.research.nodes import (
    ResearchNode,
    ReflectionNode,
    EvaluatorNode,
    FactCheckNode,
    FinalEvaluationNode,
)

from workflows.research.router import (
    evaluation_router,
)

from workflows.research.state import (
    ResearchWorkflowState,
)


class ResearchWorkflow(
    BaseWorkflow,
):

    def __init__(
        self,
        container: Container,
    ):
        self.container = container

    def build(self):

        graph = StateGraph(
            ResearchWorkflowState
        )

        #
        # Nodes
        #

        graph.add_node(
            "research",
            ResearchNode(
                self.container.research_agent
            ),
        )

        graph.add_node(
            "reflection",
            ReflectionNode(
                self.container.reflection_agent
            ),
        )

        graph.add_node(
            "evaluation",
            EvaluatorNode(
                self.container.evaluation_agent
            ),
        )

        graph.add_node(
            "fact_check",
            FactCheckNode(
                self.container.fact_check_agent
            ),
        )

        graph.add_node(
            "final_evaluation",
            FinalEvaluationNode(
                self.container.final_evaluation_agent
            ),
        )

        #
        # Main Flow
        #

        graph.add_edge(
            START,
            "research",
        )

        graph.add_edge(
            "research",
            "reflection",
        )

        graph.add_edge(
            "reflection",
            "evaluation",
        )

        #
        # Revision Loop
        #

        graph.add_conditional_edges(
            "evaluation",
            evaluation_router,
            {
                "research": "research",
                "fact_check": "fact_check",
            },
        )

        #
        # Final Validation Flow
        #

        graph.add_edge(
            "fact_check",
            "final_evaluation",
        )

        graph.add_edge(
            "final_evaluation",
            END,
        )

        return graph.compile()