from tools.base import BaseTool


class ToolRegistry:
    """
    Simple name-keyed registry for BaseTool instances.

    Tools are registered by the Container at startup and looked up by
    name during agent tool execution. The registry also provides the
    descriptions() method used by the LLM during tool planning.
    """

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Add a tool to the registry, keyed by tool.name."""
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        """
        Retrieve a tool by name.

        Raises
        ------
        KeyError : If no tool with that name has been registered.
        """
        return self._tools[name]

    def all(self) -> list[BaseTool]:
        """Return all registered tools."""
        return list(self._tools.values())

    def descriptions(self) -> list[dict]:
        """
        Return a list of tool descriptors for use in LLM tool-planning prompts.

        Each descriptor contains name, description, and the JSON schema
        of the tool's input model.
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "schema": tool.schema,
            }
            for tool in self.all()
        ]
