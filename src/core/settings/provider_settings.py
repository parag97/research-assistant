from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class ProviderSettings(BaseSettings):

    google_api_key: str

    openai_api_key: str | None = None

    anthropic_api_key: str | None = None

    open_router_api_key: str | None = None

    # ------------------------------------------------------------------
    # Langfuse OTLP credentials
    # Langfuse exposes a standard OTLP/HTTP endpoint for traces.
    # Auth is HTTP Basic: base64(public_key:secret_key) in the header.
    # ------------------------------------------------------------------
    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    langfuse_host: str = "https://cloud.langfuse.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
