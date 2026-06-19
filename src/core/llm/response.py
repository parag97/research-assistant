from pydantic import BaseModel
from core.llm.models import LLMProviderType


class LLMResponse(BaseModel):
    content: str

    model: str

    provider: LLMProviderType

    latency_ms: float | None = None

    input_tokens: int | None = None

    output_tokens: int | None = None