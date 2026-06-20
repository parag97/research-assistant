import asyncio

from core.dependencies.container import Container


async def main():

    container = Container()

    agent = (
        container
        .research_agent
    )

    result = await agent.run(
        query=(
            f'Read the url and summarize: https://en.wikipedia.org/wiki/Agentic_AI')
    )
    

    print("\n=== FINAL ARTIFACT ===")
    print(result)


if __name__ == "__main__":
    asyncio.run(
        main()
    )