from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response, APIRouter
import time

router = APIRouter(prefix="/metrics", tags=["observability"])

# -----------------------------
# Define metrics
# -----------------------------

# Count of raw events ingested
RAW_EVENTS_INGESTED = Counter(
    "raw_events_ingested_total",
    "Total number of raw events ingested",
)

# Count of raw events processed successfully
RAW_EVENTS_PROCESSED = Counter(
    "raw_events_processed_total",
    "Total number of raw events processed successfully",
)

# Count of failed events
RAW_EVENTS_FAILED = Counter(
    "raw_events_failed_total",
    "Total number of raw events that failed processing",
)

# Histogram of processing duration
RAW_EVENT_PROCESSING_DURATION = Histogram(
    "raw_event_processing_seconds",
    "Time spent processing a single raw event",
)


# -----------------------------
# Metrics endpoint
# -----------------------------
@router.get("/")
async def metrics() -> Response:
    """
    Prometheus metrics endpoint.
    """
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


# -----------------------------
# Helper functions to update metrics
# -----------------------------

def track_ingested_event():
    RAW_EVENTS_INGESTED.inc()


def track_processed_event(duration: float):
    RAW_EVENTS_PROCESSED.inc()
    RAW_EVENT_PROCESSING_DURATION.observe(duration)


def track_failed_event():
    RAW_EVENTS_FAILED.inc()
