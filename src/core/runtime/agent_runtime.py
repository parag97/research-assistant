from dataclasses import dataclass

from core.llm.base import LLMProvider


@dataclass(slots=True)
class AgentRuntime:

    llm: LLMProvider

    # future

    memory: object | None = None

    search: object | None = None

    observability: object | None = None