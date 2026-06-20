import asyncio

from tools.datetime.tool import DateTimeTool


async def main():

    tool = DateTimeTool()

    print("=== TOOL INFO ===")
    print(tool.name)
    print(tool.description)

    print("\n=== SCHEMA ===")
    print(tool.schema)

    print("\n=== EXECUTION ===")

    result = await tool.execute(
        timezone="UTC"
        , format="%d/%m/%Y, %H:%M:%S"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(
        main()
    )