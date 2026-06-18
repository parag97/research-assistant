import asyncio

from core.llm.factory import get_llm


async def main():

    llm = get_llm()

    response = await llm.invoke(
        "What is the capital of India?"
    )

    print(response.model_dump())


if __name__ == "__main__":
    asyncio.run(main())