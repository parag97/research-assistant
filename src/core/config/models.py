from pydantic import BaseModel

from core.llm.models import LLMProviderType


class AppConfig(BaseModel):
    name: str
    environment: str


class LLMConfig(BaseModel):
    default_provider: LLMProviderType
    default_model: str


class ResearchConfig(BaseModel):
    max_sources: int = 10


class MemoryConfig(BaseModel):
    top_k: int = 5


class Config(BaseModel):
    app: AppConfig
    llm: LLMConfig
    research: ResearchConfig
    memory: MemoryConfig