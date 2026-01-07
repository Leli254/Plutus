from datetime import datetime
from time import perf_counter

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db.models.raw_event import RawEvent
from db.models.processed_event import ProcessedEvent
from db.models.failed_event import FailedEvent
from db.enums import EventStatus
from app.core.logging import get_logger
from observability.tracing import get_tracer
from observability.metrics import (
    track_processed_event,
    track_failed_event,
)

logger = get_logger("processing.service")
tracer = get_tracer()


async def normalize_payload(raw_payload: dict) -> dict:
    """
    Placeholder for business normalization logic.
    Transform raw payload to canonical format.
    """
    normalized = {k.lower(): v for k, v in raw_payload.items()}
    return normalized


async def process_raw_event(
    raw_event_id: str,
    session: AsyncSession,
    handler_name: str = "default",
) -> None:
    """
    Process a single RawEvent.

    Steps:
    1. Fetch the RawEvent
    2. Normalize payload
    3. Insert into ProcessedEvent
    4. Update RawEvent.status and processed_at
    5. On failure, insert into FailedEvent
    """

    # ---- TRACE SPAN START ----
    with tracer.start_as_current_span("process_raw_event") as span:
        span.set_attribute("raw_event.id", str(raw_event_id))
        span.set_attribute("handler.name", handler_name)

        start_time = perf_counter()

        # Fetch the raw event
        result = await session.execute(
            select(RawEvent).where(RawEvent.id == raw_event_id)
        )
        raw_event: RawEvent | None = result.scalar_one_or_none()

        if not raw_event:
            span.set_attribute("raw_event.exists", False)
            logger.error("raw_event.not_found", raw_event_id=raw_event_id)
            return

        span.set_attribute("raw_event.status", raw_event.status)

        if raw_event.status == EventStatus.PROCESSED:
            span.set_attribute("raw_event.skipped", True)
            logger.info(
                "raw_event.already_processed",
                raw_event_id=raw_event_id,
            )
            return

        try:
            # Normalize payload
            normalized_payload = await normalize_payload(raw_event.payload)

            # Persist processed event
            processed_event = ProcessedEvent(
                raw_event_id=raw_event.id,
                handler_name=handler_name,
                normalized_payload=normalized_payload,
                processed_at=datetime.utcnow(),
            )
            session.add(processed_event)

            # Update raw_event status
            raw_event.status = EventStatus.PROCESSED
            raw_event.processed_at = datetime.utcnow()

            await session.commit()

            duration = perf_counter() - start_time
            track_processed_event(duration)

            span.set_attribute("processing.duration_sec", duration)
            span.set_attribute("raw_event.processed", True)

            logger.info(
                "raw_event.processed",
                raw_event_id=raw_event.id,
                handler=handler_name,
            )

        except SQLAlchemyError as e:
            await session.rollback()

            # Persist failed event
            failed_event = FailedEvent(
                raw_event_id=raw_event.id,
                error_type=type(e).__name__,
                error_message=str(e),
                retry_count=0,
                failed_at=datetime.utcnow(),
            )
            session.add(failed_event)

            raw_event.status = EventStatus.FAILED
            raw_event.processed_at = datetime.utcnow()

            await session.commit()

            track_failed_event()

            span.record_exception(e)
            span.set_attribute("raw_event.processed", False)
            span.set_attribute("raw_event.failed", True)

            logger.error(
                "raw_event.processing_failed",
                raw_event_id=raw_event.id,
                handler=handler_name,
                error=str(e),
            )
