from dataclasses import dataclass

from core.llm.base import LLMProvider
from core.observability.tracer import WorkflowTracer
from tools.registry import ToolRegistry


@dataclass(slots=True)
class AgentRuntime:
    """
    Shared dependency bundle injected into every agent.

    Agents receive a single AgentRuntime rather than individual dependencies
    so adding new capabilities (memory, search) does not require changing
    every agent constructor.

    Fields
    ------
    llm           : The active LLM provider (Ollama, Google, etc.).
    tools         : Registry of available tools the agent may call.
    observability : Tracer that records node execution events.
    memory        : Reserved for future memory/retrieval integration.
    search        : Reserved for future external search integration.
    """

    llm: LLMProvider
    tools: ToolRegistry
    observability: WorkflowTracer

    # Placeholders for future capabilities
    memory: object | None = None
    search: object | None = None
