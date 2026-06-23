from core.observability.model import TraceEvent
from opentelemetry import trace


class Tracer:

    def __init__(
        self,
        service_name: str,
    ):
        self._tracer = (
            trace.get_tracer(
                service_name
            )
        )

    def span(
        self,
        name: str,
    ):
        return self._tracer.start_as_current_span(
            name
        )


class PremitiveWorkflowTracer:
    """
    In-memory store for TraceEvents emitted during a workflow run.

    Injected into AgentRuntime and written to by the @tracer_node decorator
    after each node execution. Callers can dump the trace at the end of a
    run to inspect timing, node order, and any failures.

    This implementation keeps events in memory only — no persistence.
    A future implementation could flush to a database or observability backend.
    """

    def __init__(self) -> None:
        self._events: list[TraceEvent] = []

    def record(self, event: TraceEvent) -> None:
        """Append a TraceEvent to the in-memory log."""
        self._events.append(event)

    def clear(self) -> None:
        """Remove all recorded events (useful between test runs)."""
        self._events.clear()

    def dump(self) -> list[TraceEvent]:
        """Return a snapshot of all recorded events."""
        return self._events.copy()
