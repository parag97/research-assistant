import asyncio

from tools.search.tool import (
    SearchTool,
)


async def main():

    tool = SearchTool()

    print(tool.name)

    print(tool.description)

    print(tool.schema())



    result = await tool.execute(
        query="agentic ai"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())