import asyncio
import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.db.models.raw_event import RawEvent
from app.processing.service import process_raw_event
from app.core.logging import get_logger
from app.db.enums import EventStatus

logger = get_logger("worker.consumer")


BATCH_SIZE = 10          # Number of events to fetch per batch
POLL_INTERVAL = 2         # Seconds to wait if no pending events


async def fetch_pending_events(session: AsyncSession, limit: int = BATCH_SIZE):
    """
    Fetch a batch of pending raw events (status = RECEIVED)
    """
    result = await session.execute(
        RawEvent.__table__.select()
        .where(RawEvent.status == EventStatus.RECEIVED)
        .limit(limit)
    )
    return [row.id for row in result.fetchall()]


async def worker_loop(name: Optional[str] = "default_worker"):
    """
    Main worker loop:
    - Continuously polls for pending events
    - Processes them asynchronously
    - Sleeps if no events found
    """
    logger.info("worker.started", worker=name)

    while True:
        async with AsyncSessionLocal() as session:
            try:
                pending_event_ids = await fetch_pending_events(session)
                if not pending_event_ids:
                    await asyncio.sleep(POLL_INTERVAL)
                    continue

                # Process each event sequentially (can be changed to asyncio.gather for concurrency)
                for event_id in pending_event_ids:
                    await process_raw_event(event_id, session, handler_name=name)

            except Exception as e:
                logger.error("worker.loop_error", error=str(e))
                await asyncio.sleep(POLL_INTERVAL)


def start_worker(name: Optional[str] = "default_worker"):
    """
    Entrypoint for running worker.
    Can be invoked via CLI, Docker container, or Celery-like integration.
    """
    try:
        asyncio.run(worker_loop(name=name))
    except KeyboardInterrupt:
        logger.info("worker.stopped", worker=name)
        logger.info("worker.exited", worker=name)