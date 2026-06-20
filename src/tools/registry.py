from tools.base import BaseTool


class ToolRegistry:

    def __init__(self):

        self._tools: dict[
            str,
            BaseTool
        ] = {}


    def register(
        self,
        tool: BaseTool,
    ):

        self._tools[
            tool.name
        ] = tool


    def get(
        self,
        name: str,
    ) -> BaseTool:

        return self._tools[name]


    def all(
        self,
    ) -> list[BaseTool]:

        return list(
            self._tools.values()
        )


    def descriptions(
        self,
    ):

        return [
            {
                "name": tool.name,
                "description":
                    tool.description,
                "schema":
                    tool.schema,
            }
            for tool
            in self.all()
        ]