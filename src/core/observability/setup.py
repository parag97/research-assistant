from opentelemetry import trace

from opentelemetry.sdk.resources import (
    Resource,
)

from opentelemetry.sdk.trace import (
    TracerProvider,
)

from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

from core.observability.tracer import Tracer

def create_tracer(
    service_name: str,
):

    resource = Resource.create(
        {
            "service.name": service_name
        }
    )

    provider = TracerProvider(
        resource=resource
    )

    provider.add_span_processor(
        SimpleSpanProcessor(
            ConsoleSpanExporter()
        )
    )

    trace.set_tracer_provider(
        provider
    )

    tracer = Tracer(service_name)

    return tracer