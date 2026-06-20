from datetime import datetime
from zoneinfo import ZoneInfo

from tools.base import BaseTool
from tools.datetime.models import DateTimeInput


class DateTimeTool(BaseTool):

    @property
    def name(self) -> str:
        return "datetime"

    @property
    def description(self) -> str:
        return (
            "Get the current date and time "
            "using a valid IANA timezone identifier "
            "such as Asia/Kolkata or "
            "America/New_York."
        )

    @property
    def input_model(self):
        return DateTimeInput

    async def execute(
        self,
        **kwargs,
    ):

        request = DateTimeInput(
            **kwargs
        )

        now = datetime.now(
            ZoneInfo(
                request.timezone
            )
        )

        return {
            "timezone": request.timezone,
            "timestamp": now.strftime(
                request.format),
            "format": request.format
            
        }