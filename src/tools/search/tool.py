from tools.base import BaseTool

from tools.search.models import (
    SearchToolInput,
)


class SearchTool(
    BaseTool
):

    @property
    def name(
        self,
    ) -> str:

        return "search"


    @property
    def description(
        self,
    ) -> str:

        return (
            "Search for information "
            "about a topic."
        )


    @property
    def input_model(
        self,
    ):

        return SearchToolInput
    @property
    def schema(self):
        return self.input_model.model_json_schema()

    async def execute(
        self,
        query: str,
    ):

        return {
            "source":
                "search",

            "query":
                query,

            "result":
                f"Mock search result "
                f"for {query}"
        }