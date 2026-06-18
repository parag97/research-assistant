from functools import cache

from core.config.service import get_config
from core.llm.models import (
    LLMProviderType,
)
from core.llm.providers.google_provider import (
    GoogleProvider,
)
from core.settings.provider_settings import (
    ProviderSettings,
)


@cache
def get_llm():

    config = get_config()

    settings = ProviderSettings()

    provider = config.llm.default_provider

    if provider == LLMProviderType.GOOGLE:
        return GoogleProvider(
            model=config.llm.default_model,
            api_key=settings.google_api_key,
        )

    raise ValueError(
        f"Unsupported provider: {provider}"
    )