from pydantic import BaseModel, Field

from core.llm.models import LLMProviderType


class AppConfig(BaseModel):
    """Top-level application identity settings."""

    name: str
    environment: str


class LLMConfig(BaseModel):
    """LLM provider and model selection."""

    default_provider: LLMProviderType
    default_model: str

    # Ollama-specific connection settings
    ollama_base_url: str = "http://localhost:11434"


class AgentConfig(BaseModel):
    """
    Retry and quality settings shared across all agents.

    max_retries        : LLM call attempts before giving up.
    structured_retries : Attempts for structured-output calls (higher because
                         small models produce malformed JSON more often).
    retry_backoff      : Base backoff in seconds; multiplied by attempt number.
    research_confidence: Default confidence score for ResearchArtifact.
    reflection_confidence: Default confidence score for ReflectionArtifact.
    fact_check_confidence: Default confidence score for FactCheckArtifact.
    """

    max_retries: int = Field(default=3, ge=1)
    structured_retries: int = Field(default=4, ge=1)
    retry_backoff: float = Field(default=1.0, ge=0.0)

    research_confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    reflection_confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    fact_check_confidence: float = Field(default=0.9, ge=0.0, le=1.0)


class WorkflowConfig(BaseModel):
    """
    Research workflow execution settings.

    max_revisions: Hard cap on research→reflection→evaluation loops.
                   Prevents infinite revision cycles.
    """

    max_revisions: int = Field(default=2, ge=1)


class ResearchConfig(BaseModel):
    """Research pipeline settings."""

    max_sources: int = Field(default=10, ge=1)


class MemoryConfig(BaseModel):
    """Memory retrieval settings."""

    top_k: int = Field(default=5, ge=1)


class ToolsConfig(BaseModel):
    """
    Tool-level execution settings.

    fetch_url_max_chars: Maximum characters returned by FetchURLTool.
                         Keeps LLM context manageable on large pages.
    """

    fetch_url_max_chars: int = Field(default=5000, ge=100)


class Config(BaseModel):
    """Root configuration object loaded from dev.yml."""

    app: AppConfig
    llm: LLMConfig
    agent: AgentConfig = Field(default_factory=AgentConfig)
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)
    research: ResearchConfig = Field(default_factory=ResearchConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    tools: ToolsConfig = Field(default_factory=ToolsConfig)
