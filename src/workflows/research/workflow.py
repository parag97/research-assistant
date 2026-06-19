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


        graph.add_node(
            "research",
            ResearchNode(
                self.container.llm
            ),
        )


        graph.add_node(
            "reflection",
            ReflectionNode(
                self.container.llm
            ),
        )


        graph.add_node(
            "evaluation",
            EvaluatorNode(
                self.container.llm
            ),
        )


        graph.add_node(
            "fact_check",
            FactCheckNode(
                self.container.llm
            ),
        )


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


        graph.add_conditional_edges(
            "evaluation",
            evaluation_router,
            {
                "research": "research",
                "fact_check": "fact_check",
            },
        )


        graph.add_edge(
            "fact_check",
            END,
        )


        return graph.compile()