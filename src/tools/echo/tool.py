from core.tools.base import BaseTool


class EchoTool(
    BaseTool
):

    @property
    def name(self):

        return "echo"


    @property
    def description(self):

        return (
            "Echo back the provided text."
        )


    async def execute(
        self,
        text: str,
    ):

        return {
            "echo": text
        }