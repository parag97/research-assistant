from enum import Enum


class LLMProviderType(str, Enum):
    """
    Supported LLM backend identifiers.

    Used in Config (dev.yml default_provider) and in LLMResponse.provider
    so traces carry a clear label of which backend produced each response.
    """

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
