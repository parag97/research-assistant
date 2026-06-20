from tools.registry import ToolRegistry
from tools.datetime.tool import DateTimeTool


registry = ToolRegistry()

registry.register(
    DateTimeTool()
)

print(
    registry.descriptions()
)