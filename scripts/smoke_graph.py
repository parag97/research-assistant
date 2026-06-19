import asyncio

from core.dependencies.container import Container

from workflows.research.workflow import (
    ResearchWorkflow,
)


async def main():

    container = Container()

    graph = ResearchWorkflow(
        container
    ).build()


    result = await graph.ainvoke(
        {
            "query":
            "Explain Agentic AI architecture"
        }
    )


    print(
        result["reflection"].content
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())