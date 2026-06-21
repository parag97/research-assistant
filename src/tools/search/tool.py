from tools.base import BaseTool
from tools.search.models import SearchToolInput


class SearchTool(BaseTool):
    """
    Stub search tool — currently returns a mock result.

    Registered but commented out in the Container until a real search
    backend (e.g. SerpAPI, Tavily) is wired in. The interface is stable
    so swapping in a real implementation only requires changing execute().
    """

    @property
    def name(self) -> str:
        return "search"

    @property
    def description(self) -> str:
        return "Search the web for information about a topic."

    @property
    def input_model(self):
        return SearchToolInput

    async def execute(self, **kwargs) -> dict:
        request = SearchToolInput(**kwargs)
        # TODO: replace with a real search backend
        return {
            "query": request.query,
            "result": f"Mock search result for: {request.query}",
        }
