import base64

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from core.observability.tracer import Tracer
from core.settings.provider_settings import ProviderSettings


def _langfuse_exporter(settings: ProviderSettings) -> OTLPSpanExporter | None:
    """
    Build an OTLPSpanExporter pointed at Langfuse's trace ingest endpoint.

    Langfuse speaks standard OTLP/HTTP — it doesn't need a custom SDK.
    Authentication is HTTP Basic Auth: the public key is the username and
    the secret key is the password, base64-encoded together as one header.

    Returns None when credentials are missing so the app still starts in
    environments (e.g. CI) that don't have Langfuse configured.
    """
    if not settings.langfuse_public_key or not settings.langfuse_secret_key:
        return None

    # base64-encode "publicKey:secretKey" — this is exactly what Langfuse
    # expects in the Authorization header, matching HTTP Basic Auth spec.
    token = base64.b64encode(
        f"{settings.langfuse_public_key}:{settings.langfuse_secret_key}".encode()
    ).decode()

    return OTLPSpanExporter(
        # Langfuse's OTLP trace endpoint — the path is fixed by their API.
        endpoint=f"{settings.langfuse_host}/api/public/otel/v1/traces",
        headers={"Authorization": f"Basic {token}"},
    )


def create_tracer(service_name: str) -> Tracer:
    """
    Build and register a global TracerProvider with two exporters:

      1. ConsoleSpanExporter  — prints every span to stdout immediately.
         Uses SimpleSpanProcessor (synchronous, fine for local console output).

      2. OTLPSpanExporter → Langfuse  — sends spans over HTTP to Langfuse.
         Uses BatchSpanProcessor (async background thread, non-blocking).
         Skipped silently if Langfuse credentials are absent.

    A TracerProvider can hold any number of SpanProcessors; they all run
    in sequence on each span. That's how we fan out to both destinations
    without any extra routing logic.

    After this function runs, any call to `trace.get_tracer(name)` anywhere
    in the process will use this provider automatically — OTel stores it
    globally via `trace.set_tracer_provider()`.
    """
    settings = ProviderSettings()

    # Resource.create() attaches key-value metadata to every span this
    # provider emits. "service.name" is the standard OTel attribute that
    # Langfuse uses to group traces under a project/service in the UI.
    resource = Resource.create({"service.name": service_name})

    provider = TracerProvider(resource=resource)

    # --- Exporter 1: Console (always on) ---------------------------------
    # SimpleSpanProcessor calls export() synchronously when a span ends.
    # That's acceptable here because ConsoleSpanExporter is just a print —
    # no I/O latency. For any real network exporter, use BatchSpanProcessor.
    provider.add_span_processor(
        SimpleSpanProcessor(ConsoleSpanExporter())
    )

    # --- Exporter 2: Langfuse via OTLP (when credentials present) --------
    # BatchSpanProcessor collects finished spans into a queue and flushes
    # them to Langfuse in the background. Your async handlers return
    # immediately; the export happens off the event loop thread.
    langfuse = _langfuse_exporter(settings)
    if langfuse:
        provider.add_span_processor(BatchSpanProcessor(langfuse))
    else:
        print(
            "[observability] LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY not set — "
            "skipping Langfuse exporter. Console output only."
        )

    # Register as the process-wide default. Every trace.get_tracer() call
    # after this point will route through this provider.
    trace.set_tracer_provider(provider)

    return Tracer(service_name)
