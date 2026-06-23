from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class ProviderSettings(BaseSettings):

    google_api_key: str

    openai_api_key: str | None = None

    anthropic_api_key: str | None = None

    open_router_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )