"""
smoke_research_workflow.py

End-to-end smoke test for the research workflow.

Builds and runs the full ResearchWorkflow graph against a simple query,
then prints the output of each pipeline stage so you can visually verify
the workflow is wired up and all agents are responding correctly.

Usage:
    uv run python scripts/smoke_research_workflow.py
"""

import asyncio
import json

from core.dependencies.container import Container


async def main() -> None:

    container = Container("research agent")

    # Use the pre-built workflow from the container so the same
    # config-driven wiring is exercised as in production.
    graph = container.research_workflow.build()

    result = await graph.ainvoke(
        {
            "query": (
                "Explain how multi-agent AI systems, be very brief, answer quickly, no more then 2 lines "
                "use planning and reflection."
            ),
            "revision_count": 0,
        }
    )
    print(result)
    # ------------------------------------------------------------------
    # Print each stage's output
    # ------------------------------------------------------------------

    print("\n========== QUERY ==========\n")
    print(result["query"])

    print("\n========== RESEARCH ==========\n")
    print(result["research"].content)

    print("\n========== REFLECTION ==========\n")
    print(result["reflection"].content)

    print("\n========== EVALUATION ==========\n")
    print(json.dumps(result["evaluation"].model_dump(), indent=2))

    print("\n========== FACT CHECK ==========\n")
    print(result["fact_check"].content)

    print("\n========== FINAL EVALUATION ==========\n")
    print(json.dumps(result["final_evaluation"].model_dump(), indent=2))

    print(f"\nRevision Count: {result['revision_count']}")

    # ------------------------------------------------------------------
    # Print the observability trace
    # ------------------------------------------------------------------

    # print("\n========== TRACE ==========\n")
    # for event in container.tracer.dump():
    #     print(
    #         f"[{event.status.upper()}] {event.node_name} "
    #         f"— {event.duration_ms:.0f}ms"
    #         + (f" — {event.error}" if event.error else "")
    #     )

    # Report any non-fatal errors accumulated in state
    errors = result.get("errors") or []
    if errors:
        print(f"\n⚠ Non-fatal errors ({len(errors)}):")
        for err in errors:
            print(f"  • {err}")


if __name__ == "__main__":
    asyncio.run(main())
