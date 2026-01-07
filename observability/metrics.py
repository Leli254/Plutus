# observability/metrics.py

from fastapi import FastAPI, Response, APIRouter
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

# -----------------------------
# Router
# -----------------------------
router = APIRouter(prefix="/metrics", tags=["observability"])

# -----------------------------
# Metrics definitions
# -----------------------------

RAW_EVENTS_INGESTED = Counter(
    "raw_events_ingested_total",
    "Total number of raw events ingested",
)

RAW_EVENTS_PROCESSED = Counter(
    "raw_events_processed_total",
    "Total number of raw events processed successfully",
)

RAW_EVENTS_FAILED = Counter(
    "raw_events_failed_total",
    "Total number of raw events that failed processing",
)

RAW_EVENT_PROCESSING_DURATION = Histogram(
    "raw_event_processing_seconds",
    "Time spent processing a single raw event",
)

# -----------------------------
# Metrics endpoint
# -----------------------------


@router.get("")
async def metrics() -> Response:
    """
    Prometheus scrape endpoint.
    """
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

# -----------------------------
# Setup hook
# -----------------------------


def setup_prometheus(app: FastAPI) -> None:
    """
    Attach Prometheus metrics to the FastAPI app.
    """
    app.include_router(router)

# -----------------------------
# Helper functions (used elsewhere)
# -----------------------------


def track_ingested_event() -> None:
    RAW_EVENTS_INGESTED.inc()


def track_processed_event(duration: float) -> None:
    RAW_EVENTS_PROCESSED.inc()
    RAW_EVENT_PROCESSING_DURATION.observe(duration)


def track_failed_event() -> None:
    RAW_EVENTS_FAILED.inc()
