from pydantic import BaseModel, Field

from tools.base import BaseTool


class EchoInput(BaseModel):
    """Input model for EchoTool."""

    text: str = Field(description="The text to echo back.")


class EchoTool(BaseTool):
    """
    Development/testing tool that echoes its input back unchanged.

    Useful for verifying that the tool-planning and execution pipeline
    is wired up correctly without making external calls.
    """

    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Echo back the provided text unchanged. Useful for testing."

    @property
    def input_model(self):
        return EchoInput

    async def execute(self, **kwargs) -> dict:
        request = EchoInput(**kwargs)
        return {"echo": request.text}
