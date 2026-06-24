from functools import cached_property

from core.config.service import get_config
from core.llm.factory import get_llm
from core.runtime.agent_runtime import AgentRuntime
from core.observability.setup import create_tracer       # single import, no duplicate
from core.observability.tracer import PrimitiveWorkflowTracer, Tracer
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

    Lifecycle
    ---------
    Create one Container per process. Call `shutdown()` before the
    process exits to flush any buffered spans to Langfuse.
    """

    def __init__(self, service_name: str):
        self.service_name = service_name

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
    def tracer(self) -> Tracer:
        # create_tracer() registers the global OTel TracerProvider and
        # returns our thin Tracer wrapper. Called once; cached_property
        # ensures the provider is only registered a single time even if
        # something accesses container.tracer multiple times.
        return create_tracer(service_name=self.service_name)

    @cached_property
    def llm(self):
        return get_llm(self.tracer)

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
            tracer=self.tracer,
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

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def shutdown(self) -> None:
        """
        Flush buffered spans and shut down the TracerProvider.

        BatchSpanProcessor holds spans in a queue and exports them in the
        background. Without an explicit shutdown() call, any spans still
        in the queue when the process exits are silently dropped and will
        never appear in Langfuse.

        Call this in your FastAPI lifespan `finally` block or at the end
        of your main() function:

            container = Container("research-assistant")
            try:
                await container.research_workflow.run(...)
            finally:
                container.shutdown()
        """
        Tracer.shutdown()
