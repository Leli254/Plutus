# workers/consumer.py

import asyncio
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import AsyncSessionLocal
from db.models.raw_event import RawEvent
from db.enums import EventStatus
from processing.service import process_raw_event

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from observability.tracing import setup_tracing, get_tracer

logger = get_logger("worker.consumer")

BATCH_SIZE = 10
POLL_INTERVAL = 2  # seconds
ERROR_BACKOFF = 5  # seconds


# =========================
# Database access
# =========================

async def fetch_pending_events(
    session: AsyncSession,
    limit: int = BATCH_SIZE,
) -> List[int]:
    """
    Fetch IDs of pending raw events.
    """
    stmt = (
        select(RawEvent.id)
        .where(RawEvent.status == EventStatus.RECEIVED)
        .limit(limit)
    )

    result = await session.execute(stmt)
    return [row[0] for row in result.all()]


# =========================
# Processing
# =========================

async def process_batch(
    worker_name: str,
    event_ids: List[int],
) -> None:
    """
    Process events one-by-one using isolated DB sessions.
    """
    tracer = get_tracer()

    for event_id in event_ids:
        with tracer.start_as_current_span("worker.process_event") as span:
            span.set_attribute("worker.name", worker_name)
            span.set_attribute("raw_event.id", event_id)

            async with AsyncSessionLocal() as session:
                await process_raw_event(
                    event_id=event_id,
                    session=session,
                    handler_name=worker_name,
                )


# =========================
# Worker loop
# =========================

async def worker_loop(worker_name: str) -> None:
    """
    Long-running worker loop (Option A).
    """
    tracer = get_tracer()

    logger.info("worker.started", worker=worker_name)

    while True:
        try:
            with tracer.start_as_current_span("worker.poll") as poll_span:
                poll_span.set_attribute("worker.name", worker_name)

                async with AsyncSessionLocal() as session:
                    event_ids = await fetch_pending_events(session)
                    poll_span.set_attribute("batch.size", len(event_ids))

                if not event_ids:
                    await asyncio.sleep(POLL_INTERVAL)
                    continue

                await process_batch(
                    worker_name=worker_name,
                    event_ids=event_ids,
                )

        except asyncio.CancelledError:
            logger.info("worker.cancelled", worker=worker_name)
            raise

        except Exception as exc:
            logger.exception(
                "worker.loop_error",
                worker=worker_name,
                error=str(exc),
            )
            await asyncio.sleep(ERROR_BACKOFF)


# =========================
# Entrypoint
# =========================

def run_worker(name: Optional[str] = None) -> None:
    """
    Entrypoint for Docker / CLI.
    """
    configure_logging()
    settings = get_settings()

    worker_name = name or "default_worker"

    if settings.tracing_enabled:
        setup_tracing(
            service_name=f"{settings.service_name}-worker",
            otlp_endpoint=settings.otlp_endpoint,
        )

    try:
        asyncio.run(worker_loop(worker_name))
    except KeyboardInterrupt:
        logger.info("worker.stopped", worker=worker_name)


if __name__ == "__main__":
    run_worker()
