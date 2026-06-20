import asyncio

from tools.search.tool import (
    SearchTool,
)


async def main():

    tool = SearchTool()

    print(tool.name)
    print("="*100)

    print(tool.description)
    print("="*100)
    print(tool.schema)
    print("="*100)


    result = await tool.execute(
        query="agentic ai"
    )

    # print(result)


if __name__ == "__main__":
    asyncio.run(main())