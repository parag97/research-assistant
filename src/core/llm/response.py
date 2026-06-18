from pydantic import BaseModel


class LLMResponse(BaseModel):
    content: str

    model: str

    provider: str

    latency_ms: float | None = None

    input_tokens: int | None = None

    output_tokens: int | None = None