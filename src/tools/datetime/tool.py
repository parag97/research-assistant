import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from tools.base import BaseTool
from tools.datetime.models import DateTimeInput

logger = logging.getLogger(__name__)


class DateTimeTool(BaseTool):
    """
    Returns the current date and time for a given IANA timezone.

    Useful for research queries that require temporal context, such as
    "what time is it in Tokyo?" or date-aware research planning.
    """

    @property
    def name(self) -> str:
        return "datetime"

    @property
    def description(self) -> str:
        return (
            "Get the current date and time for a given IANA timezone identifier. "
            "Examples of valid timezones: UTC, America/New_York, Asia/Kolkata, Europe/London."
        )

    @property
    def input_model(self):
        return DateTimeInput

    async def execute(self, **kwargs) -> dict:

        request = DateTimeInput(**kwargs)

        now = datetime.now(ZoneInfo(request.timezone))

        return {
            "timezone": request.timezone,
            "timestamp": now.strftime(request.format),
            "format": request.format,
        }
