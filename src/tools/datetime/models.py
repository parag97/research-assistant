from pydantic import BaseModel, Field


class DateTimeInput(BaseModel):
    """Input model for DateTimeTool."""

    timezone: str = Field(
        default="UTC",
        description=(
            "A valid IANA timezone identifier. "
            "Examples: UTC, America/New_York, Europe/London, Asia/Kolkata. "
            "See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
        ),
    )

    format: str = Field(
        default="%d/%m/%Y %H:%M:%S",
        description=(
            "strftime format string for the output timestamp. "
            "Default: '%d/%m/%Y %H:%M:%S' (e.g. 21/06/2026 14:30:00)."
        ),
    )
