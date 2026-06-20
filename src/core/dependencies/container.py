from functools import cached_property

from core.llm.factory import get_llm
from core.runtime.agent_runtime import AgentRuntime
from tools.registry import ToolRegistry

from agents.research.agent import ResearchAgent
from agents.reflection.agent import ReflectionAgent
from agents.evaluation.agent import EvaluationAgent
from agents.fact_check.agent import FactCheckAgent
from agents.final_evaluation.agent import FinalEvaluationAgent

from tools.search.tool import SearchTool
from tools.datetime.tool import DateTimeTool
from tools.calculator.tool import CalculatorTool
from tools.fetch_url_tool.tool import FetchURLTool

from core.observability.tracer import WorkflowTracer

class Container:

    @cached_property
    def llm(self):
        return get_llm()

    @cached_property
    def tool_registry(self):

        registry = ToolRegistry()

        registry.register(
            DateTimeTool()
        )

        # registry.register(
        #     SearchTool()
        # )

        registry.register(
            CalculatorTool()
        )

        registry.register(
            FetchURLTool()
                        )

        return registry

    @cached_property
    def tracer(self):
        return WorkflowTracer()

    @cached_property
    def runtime(self):
        return AgentRuntime(
            llm=self.llm,
            tools=self.tool_registry,
            observability=self.tracer
        )

    @cached_property
    def research_agent(self):
        return ResearchAgent(self.runtime)

    @cached_property
    def reflection_agent(self):
        return ReflectionAgent(self.runtime)

    @cached_property
    def evaluation_agent(self):
        return EvaluationAgent(self.runtime)

    @cached_property
    def fact_check_agent(self):
        return FactCheckAgent(self.runtime)

    @cached_property
    def final_evaluation_agent(self):
        return FinalEvaluationAgent(self.runtime)
