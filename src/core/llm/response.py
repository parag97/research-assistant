from pydantic import BaseModel

from core.llm.models import LLMProviderType


class LLMResponse(BaseModel):
    """
    Normalised response returned by every LLMProvider.invoke() call.

    Wraps the raw provider response so the rest of the codebase is
    decoupled from provider-specific response formats.

    Fields
    ------
    content      : The generated text from the model.
    model        : Identifier of the model that produced the response.
    provider     : Which backend was used (ollama, google, etc.).
    latency_ms   : Wall-clock time for the request in milliseconds.
    input_tokens : Prompt token count if reported by the provider.
    output_tokens: Completion token count if reported by the provider.
    """

    content: str
    model: str
    provider: LLMProviderType
    latency_ms: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
