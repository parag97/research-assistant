from datetime import UTC, datetime
from functools import wraps

from core.observability.model import TraceEvent


def tracer_node(node_name: str):
    """
    Decorator that wraps a LangGraph node's __call__ method with tracing.

    Records start time, end time, duration, and whether the node
    succeeded or raised an exception. Emits a TraceEvent to the
    runtime's observability backend regardless of outcome.

    Usage:
        @tracer_node("ResearchNode")
        async def __call__(self, state): ...

    Requires:
        self.agent.runtime.observability to be set on the node instance.
    """

    def decorator(func):

        @wraps(func)
        async def wrapper(self, state):

            start_time = datetime.now(UTC)
            status = "success"
            error_message = None

            try:
                # Execute the wrapped node function
                result = await func(self, state)

            except Exception as exc:
                # Capture failure details before re-raising
                status = "failure"
                error_message = f"{type(exc).__name__}: {exc}"
                raise

            finally:
                # Always record the trace, even on failure
                end_time = datetime.now(UTC)
                duration_ms = (end_time - start_time).total_seconds() * 1000

                try:
                    self.agent.runtime.observability.record(
                        TraceEvent(
                            workflow_id="workflow",
                            node_name=node_name,
                            start_time=start_time,
                            end_time=end_time,
                            duration_ms=round(duration_ms, 2),
                            status=status,
                            error=error_message,
                        )
                    )
                except Exception as obs_exc:
                    # Observability must never crash the workflow
                    print(
                        f"[observability] Failed to record trace for "
                        f"{node_name}: {obs_exc}"
                    )

            return result

        return wrapper

    return decorator
