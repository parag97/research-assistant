from time import timezone
from pydantic import BaseModel, Field


class DateTimeInput(BaseModel):
    timezone: str = Field(
        default= 'UTC', 
        description=(
            "Never give timezones like: Asia/Mumbai "
            "Always use valid IANA timezone identifiers. "

            "Valid IANA timezone identifier. "
            "Examples: Asia/Kolkata, "
            "America/New_York, Europe/London, UTC. "
            "Do not use city names."
            "See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
            " for a list of valid timezone identifiers."
            "list of bad time zones Asia/Mumbai it should be Asia/Kolkata for all cities in india "
            " use Asia/Kolkata for all cities in india instead of Asia/Calcutta or Asia/Mumbai "
            "Asia/Calcutta should be Asia/Kolkata"

            )
        )
    format: str = Field(
        default= '%d/%m/%Y %H:%M:%S',
        description='DateTime format'
        )
