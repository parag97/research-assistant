from functools import cache

from core.config.service import get_config
from core.llm.models import LLMProviderType
from core.llm.providers.google_provider import GoogleProvider
from core.llm.providers.ollama_provider import OllamaProvider
from core.settings.provider_settings import ProviderSettings


@cache
def get_llm():
    """
    Instantiate and cache the configured LLM provider.

    Provider and model are read from the active Config.
    API keys are read from ProviderSettings (environment / .env file).
    """

    config = get_config()
    settings = ProviderSettings()
    provider = config.llm.default_provider

    if provider == LLMProviderType.GOOGLE:
        return GoogleProvider(
            model=config.llm.default_model,
            api_key=settings.google_api_key,
        )

    if provider == LLMProviderType.OLLAMA:
        return OllamaProvider(
            model=config.llm.default_model,
            base_url=config.llm.ollama_base_url,
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")
