import asyncio
import json

from core.dependencies.container import Container

from workflows.research.workflow import ResearchWorkflow


async def main():

    container = Container()

    workflow = ResearchWorkflow(
        container=container,
    )

    graph = workflow.build()

    result = await graph.ainvoke(
        {
            "query": (
                "Explain how AI agents work"
                "use planning and reflection."
                "Dont use internet"
            ),
            "revision_count": 0,
        }
    )

    


    print("\n========== QUERY ==========\n")
    print(
        result["query"]
    )


    print("\n========== RESEARCH ==========\n")
    print(
        result["research"].content
    )


    print("\n========== REFLECTION ==========\n")
    print(
        result["reflection"].content
    )


    print("\n========== EVALUATION ==========\n")

    print(
        json.dumps(
            result["evaluation"].model_dump(),
            indent=2,
        )
    )


    print("\n========== FACT CHECK ==========\n")
    print(
        result["fact_check"].content
    )

    print("\n========== FINAL EVALUATION ==========\n")
    print(
        json.dumps(
            result["final_evaluation"].model_dump(),
            indent=2,
        )
    )

    print(
        "\nRevision Count:",
        result["revision_count"],
    )


if __name__ == "__main__":
    asyncio.run(main())