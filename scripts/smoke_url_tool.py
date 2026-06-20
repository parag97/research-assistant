import asyncio

from tools.fetch_url_tool.tool import FetchURLTool


async def main():

    tool = FetchURLTool()

    result = await tool.execute(
        url="https://example.com"
    )

    print(result["url"])
    print(result["content"][:500])


if __name__ == "__main__":
    asyncio.run(main())