from pydantic import BaseModel, Field


class FetchURLInput(BaseModel):
    
    url: str = Field(default=None, description="The URL to fetch")

    depth: int = Field(1, description="The depth to fetch")
