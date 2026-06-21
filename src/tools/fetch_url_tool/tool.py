import logging
import urllib.request

from tools.base import BaseTool
from tools.fetch_url_tool.model import FetchURLInput

logger = logging.getLogger(__name__)


class FetchURLTool(BaseTool):
    """
    Fetches the text content of a URL and returns a truncated result.

    max_chars controls how much content is returned to the LLM.
    Injected by the Container as a plain int — this class never reads config.
    """

    def __init__(self, max_chars: int) -> None:
        self._max_chars = max_chars

    @property
    def name(self) -> str:
        return "fetch_url"

    @property
    def description(self) -> str:
        return "Fetch a URL and return its text content."

    @property
    def input_model(self):
        return FetchURLInput

    async def execute(self, **kwargs):

        request = FetchURLInput(**kwargs)

        try:
            with urllib.request.urlopen(request.url) as response:
                content = response.read().decode("utf-8", errors="ignore")

            return {
                "url": request.url,
                "content": content[: self._max_chars],
            }

        except Exception as exc:
            logger.warning("FetchURLTool failed for '%s': %s", request.url, exc)
            return {
                "url": request.url,
                "content": f"Failed to fetch URL: {exc}",
            }
