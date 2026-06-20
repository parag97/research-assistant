from core.dependencies.container import Container


container = Container()

print(
    container.tool_registry
    .descriptions()
)