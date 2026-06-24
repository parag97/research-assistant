from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

from core.observability.model import TraceEvent


class Tracer:
    """
    Thin wrapper around an OpenTelemetry tracer instance.

    We wrap rather than use OTel directly so the rest of the codebase
    never imports opentelemetry — only this module does. That makes it
    easy to swap the underlying tracing library without touching agents
    or workflows.
    """

    def __init__(self, service_name: str) -> None:
        # get_tracer() looks up the globally registered TracerProvider
        # (set by create_tracer() in setup.py) and returns an
        # instrumentation-scoped tracer. The service_name is used as the
        # instrumentation scope name visible in Langfuse.
        self._tracer = trace.get_tracer(service_name)

    def span(self, name: str):
        """
        Return a context manager that opens a new OTel span.

        Usage (from decorators.py):
            with self.agent.runtime.tracer.span("ResearchNode"):
                ...

        The span is automatically parented to whatever span is currently
        active on the context var — so nested calls produce a proper tree
        in Langfuse without any manual parent wiring.
        """
        return self._tracer.start_as_current_span(name)

    @staticmethod
    def shutdown() -> None:
        """
        Flush all pending spans and shut down the global TracerProvider.

        BatchSpanProcessor buffers spans in memory and exports them in
        the background. If the process exits before the buffer drains,
        those spans are lost silently. Call this on app shutdown to make
        sure every span reaches Langfuse.

        Safe to call even if no BatchSpanProcessor is registered — the
        SDK no-ops in that case.
        """
        provider = trace.get_tracer_provider()
        if isinstance(provider, TracerProvider):
            provider.shutdown()


class PrimitiveWorkflowTracer:
    """
    In-memory store for TraceEvents emitted during a workflow run.

    Injected into AgentRuntime and written to by the @trace_node decorator
    after each node execution. Callers can dump the trace at the end of a
    run to inspect timing, node order, and any failures.

    This is separate from the OTel tracer — it's a lightweight internal
    audit log, not a span emitter. Useful for unit tests and for
    inspecting workflow execution without an observability backend.
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


# Backward-compat alias — remove once all callsites are updated
PremitiveWorkflowTracer = PrimitiveWorkflowTracer
