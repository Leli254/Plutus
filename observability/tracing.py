from opentelemetry import trace
from opentelemetry.trace import Tracer
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    BatchSpanProcessor,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from fastapi import FastAPI

tracer: Tracer | None = None


def setup_tracing(app: FastAPI, service_name: str = "ingestor-service", otlp_endpoint: str | None = None):
    """
    Initialize OpenTelemetry tracing for FastAPI + async workers.

    - Automatically instruments HTTP requests
    - Adds a tracer for manual spans
    - Can export to OTLP/Jaeger/Console
    """

    global tracer

    # 1. Configure TracerProvider
    resource = Resource.create(attributes={"service.name": service_name})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # 2. Add exporters
    # Console exporter (dev/debug)
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    # Optional: OTLP exporter (Jaeger/Collector)
    if otlp_endpoint:
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    # 3. Get global tracer
    tracer = trace.get_tracer(service_name)

    # 4. Instrument FastAPI automatically
    FastAPIInstrumentor.instrument_app(app)
    app.add_middleware(OpenTelemetryMiddleware)

    return tracer


def get_tracer() -> Tracer:
    if tracer is None:
        raise RuntimeError(
            "Tracer not initialized. Call setup_tracing(app) first.")
    return tracer
