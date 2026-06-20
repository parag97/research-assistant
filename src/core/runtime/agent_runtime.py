from dataclasses import dataclass

from core.llm.base import LLMProvider

from tools.registry import ToolRegistry

from core.observability.tracer import WorkflowTracer

@dataclass(slots=True)
class AgentRuntime:

    llm: LLMProvider

    tools: ToolRegistry

    observability: WorkflowTracer

    # future

    memory: object | None = None

    search: object | None = None
