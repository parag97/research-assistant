from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class ArtifactType(str, Enum):
    """Discriminator enum used by the Artifact base class."""

    RESEARCH = "research"
    REFLECTION = "reflection"
    FACT_CHECK = "fact_check"
    FINAL_REPORT = "final_report"


class Source(BaseModel):
    """
    A single source document referenced by an artifact.

    Fields
    ------
    title   : Human-readable label for the source.
    path    : Optional file path or URL.
    content : The relevant text excerpt from the source.
    """

    title: str
    path: str | None = None
    content: str


class Artifact(BaseModel):
    """
    Base class for all artifacts produced during the research workflow.

    Subclasses specialise artifact_type so the type is embedded in the
    serialised form and each artifact is self-describing.

    Fields
    ------
    artifact_id  : UUID assigned at creation.
    created_at   : UTC timestamp of creation.
    artifact_type: Discriminator indicating which pipeline stage created it.
    content      : The primary text output of the generating agent.
    confidence   : Optional 0–1 quality score set by the generating agent.
    sources      : Documents the agent drew from (currently unused).
    metadata     : Arbitrary key-value pairs for extensibility.
    trace_id     : Links the artifact to a specific observability trace.
    workflow_id  : Links the artifact to a specific workflow run.
    """

    artifact_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    artifact_type: ArtifactType
    content: str
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    sources: list[Source] = Field(default_factory=list)
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)
    trace_id: str | None = None
    workflow_id: str | None = None


class ResearchArtifact(Artifact):
    """Output of the ResearchAgent — the primary research content."""

    artifact_type: ArtifactType = ArtifactType.RESEARCH


class ReflectionArtifact(Artifact):
    """Output of the ReflectionAgent — critique of the research."""

    artifact_type: ArtifactType = ArtifactType.REFLECTION


class FactCheckArtifact(Artifact):
    """Output of the FactCheckAgent — accuracy validation report."""

    artifact_type: ArtifactType = ArtifactType.FACT_CHECK


class FinalReportArtifact(Artifact):
    """Output of a final report generation step (reserved for future use)."""

    artifact_type: ArtifactType = ArtifactType.FINAL_REPORT
