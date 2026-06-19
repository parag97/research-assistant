from pydantic import BaseModel, Field

from core.models.artifact import (
    FactCheckArtifact,
    FinalReportArtifact,
    ReflectionArtifact,
    ResearchArtifact,
)


class WorkflowState(BaseModel):
    query: str

    research: ResearchArtifact | None = None

    reflection: ReflectionArtifact | None = None

    fact_check: FactCheckArtifact | None = None

    final_report: FinalReportArtifact | None = None

    errors: list[str] = Field(
        default_factory=list
    )


