from pydantic import BaseModel, Field


class SearchToolInput(BaseModel):
    """Input model for SearchTool."""

    query: str = Field(
        description="The search query to look up information about."
    )
