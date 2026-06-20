from dataclasses import dataclass

from core.llm.base import LLMProvider

from tools.registry import ToolRegistry

@dataclass(slots=True)
class AgentRuntime:

    llm: LLMProvider

    tools: ToolRegistry

    # future

    memory: object | None = None

    search: object | None = None

    observability: object | None = None