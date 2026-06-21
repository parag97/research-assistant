from functools import cached_property

from core.config.service import get_config
from core.llm.factory import get_llm
from core.runtime.agent_runtime import AgentRuntime
from core.observability.tracer import WorkflowTracer
from tools.registry import ToolRegistry

from tools.datetime.tool import DateTimeTool
from tools.calculator.tool import CalculatorTool
from tools.fetch_url_tool.tool import FetchURLTool

from agents.research.agent import ResearchAgent
from agents.reflection.agent import ReflectionAgent
from agents.evaluation.agent import EvaluationAgent
from agents.fact_check.agent import FactCheckAgent
from agents.final_evaluation.agent import FinalEvaluationAgent

from workflows.research.workflow import ResearchWorkflow


class Container:
    """
    Dependency injection root.

    Reads the active Config once and distributes individual parameter
    values to each object it constructs. Nothing downstream receives a
    config object — only plain primitives and domain objects.
    """

    # ------------------------------------------------------------------
    # Config (read once, used throughout)
    # ------------------------------------------------------------------

    @cached_property
    def _config(self):
        return get_config()

    # ------------------------------------------------------------------
    # Infrastructure
    # ------------------------------------------------------------------

    @cached_property
    def llm(self):
        return get_llm()

    @cached_property
    def tracer(self):
        return WorkflowTracer()

    @cached_property
    def tool_registry(self):
        cfg = self._config.tools

        registry = ToolRegistry()
        registry.register(DateTimeTool())
        registry.register(CalculatorTool())
        registry.register(FetchURLTool(max_chars=cfg.fetch_url_max_chars))
        return registry

    @cached_property
    def runtime(self):
        return AgentRuntime(
            llm=self.llm,
            tools=self.tool_registry,
            observability=self.tracer,
        )

    # ------------------------------------------------------------------
    # Agents
    # ------------------------------------------------------------------

    @cached_property
    def research_agent(self):
        cfg = self._config.agent
        return ResearchAgent(
            runtime=self.runtime,
            max_retries=cfg.max_retries,
            structured_retries=cfg.structured_retries,
            retry_backoff=cfg.retry_backoff,
            confidence=cfg.research_confidence,
        )

    @cached_property
    def reflection_agent(self):
        cfg = self._config.agent
        return ReflectionAgent(
            runtime=self.runtime,
            max_retries=cfg.max_retries,
            retry_backoff=cfg.retry_backoff,
            confidence=cfg.reflection_confidence,
        )

    @cached_property
    def evaluation_agent(self):
        cfg = self._config.agent
        return EvaluationAgent(
            runtime=self.runtime,
            max_retries=cfg.structured_retries,
            retry_backoff=cfg.retry_backoff,
        )

    @cached_property
    def fact_check_agent(self):
        cfg = self._config.agent
        return FactCheckAgent(
            runtime=self.runtime,
            max_retries=cfg.max_retries,
            retry_backoff=cfg.retry_backoff,
            confidence=cfg.fact_check_confidence,
        )

    @cached_property
    def final_evaluation_agent(self):
        cfg = self._config.agent
        return FinalEvaluationAgent(
            runtime=self.runtime,
            max_retries=cfg.structured_retries,
            retry_backoff=cfg.retry_backoff,
        )

    # ------------------------------------------------------------------
    # Workflows
    # ------------------------------------------------------------------

    @cached_property
    def research_workflow(self):
        return ResearchWorkflow(
            research_agent=self.research_agent,
            reflection_agent=self.reflection_agent,
            evaluation_agent=self.evaluation_agent,
            fact_check_agent=self.fact_check_agent,
            final_evaluation_agent=self.final_evaluation_agent,
            max_revisions=self._config.workflow.max_revisions,
        )
