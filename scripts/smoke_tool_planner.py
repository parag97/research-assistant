import asyncio

from core.dependencies.container import (
    Container,
)

from tools.models import (
    ToolPlan,
)


async def main():

    container = Container()

    tools = (
        container
        .tool_registry
        .descriptions()
    )

    prompt = f"""
    Available Tools:

    {tools}

    User Query:

    What is Agentic AI?

    Return tool calls.
    """

    result = await (
        container
        .llm
        .structured(
            prompt=prompt,
            schema=ToolPlan,
        )
    )

    print(
        result.model_dump_json(
            indent=2
        )
    )


if __name__ == "__main__":
    asyncio.run(main())