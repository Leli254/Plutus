# observability/tracing.py

from typing import Optional

from fastapi import FastAPI
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

# ---- INTERNAL STATE ----
_tracer: Optional[Tracer] = None
_initialized: bool = False


def setup_tracing(
    app: Optional[FastAPI] = None,
    *,
    service_name: str = "plutus",
    otlp_endpoint: Optional[str] = None,
) -> Tracer:
    """
    Initialize OpenTelemetry tracing.

    Can be safely called:
    - from FastAPI startup
    - from worker entrypoints
    - multiple times (idempotent)

    Parameters:
        app: FastAPI app (optional, only for HTTP instrumentation)
        service_name: logical service name
        otlp_endpoint: optional OTLP collector endpoint
    """

    global _tracer, _initialized

    if _initialized:
        return _tracer  # type: ignore

    # ---- Resource ----
    resource = Resource.create(
        attributes={"service.name": service_name}
    )

    # ---- Tracer Provider ----
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # ---- Exporters ----
    provider.add_span_processor(
        SimpleSpanProcessor(ConsoleSpanExporter())
    )

    if otlp_endpoint:
        provider.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporter(endpoint=otlp_endpoint)
            )
        )

    # ---- Tracer ----
    _tracer = trace.get_tracer(service_name)
    _initialized = True

    # ---- FastAPI Instrumentation ----
    if app is not None:
        FastAPIInstrumentor.instrument_app(app)
        app.add_middleware(OpenTelemetryMiddleware)

    return _tracer


def get_tracer() -> Tracer:
    """
    Safe tracer accessor.

    - Never raises
    - Returns a no-op tracer if tracing is not initialized
    """
    if _tracer is not None:
        return _tracer

    # Return a NOOP tracer instead of crashing
    return trace.get_tracer("noop")
