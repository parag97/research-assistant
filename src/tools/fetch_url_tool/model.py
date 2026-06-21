from pydantic import BaseModel, Field


class FetchURLInput(BaseModel):
    """Input model for FetchURLTool."""

    url: str = Field(
        description="The fully-qualified URL to fetch (must start with http:// or https://)."
    )
