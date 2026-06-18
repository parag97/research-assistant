from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class ArtifactType(str, Enum):
    RESEARCH = "research"
    REFLECTION = "reflection"
    FACT_CHECK = "fact_check"
    FINAL_REPORT = "final_report"


class Source(BaseModel):
    title: str
    path: str | None = None
    content: str


class Artifact(BaseModel):
    artifact_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    artifact_type: ArtifactType

    content: str

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    sources: list[Source] = Field(
        default_factory=list
    )

    metadata: dict[str, str | int | float | bool] = Field(
        default_factory=dict
    )

    trace_id: str | None = None
    workflow_id: str | None = None


class ResearchArtifact(Artifact):
    artifact_type: ArtifactType = ArtifactType.RESEARCH


class ReflectionArtifact(Artifact):
    artifact_type: ArtifactType = ArtifactType.REFLECTION


class FactCheckArtifact(Artifact):
    artifact_type: ArtifactType = ArtifactType.FACT_CHECK


class FinalReportArtifact(Artifact):
    artifact_type: ArtifactType = ArtifactType.FINAL_REPORT