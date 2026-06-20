from pydantic import BaseModel
from pydantic import Field


class SearchToolInput(
    BaseModel
):

    query: str = Field(
        description=
        "Search query"
    )