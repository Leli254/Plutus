from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from app.db.models.raw_event import RawEvent
from app.db.models.processed_event import ProcessedEvent
from app.db.models.failed_event import FailedEvent
from app.db.enums import EventStatus
from app.core.logging import get_logger

logger = get_logger("processing.service")


async def normalize_payload(raw_payload: dict) -> dict:
    """
    Placeholder for business normalization logic.
    Transform raw payload to canonical format.
    """
    # Example transformation: ensure all keys are lowercase
    normalized = {k.lower(): v for k, v in raw_payload.items()}
    return normalized


async def process_raw_event(
    raw_event_id: str, session: AsyncSession, handler_name: str = "default"
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

    # Fetch the raw event
    result = await session.execute(
        select(RawEvent).where(RawEvent.id == raw_event_id)
    )
    raw_event: RawEvent | None = result.scalar_one_or_none()

    if not raw_event:
        logger.error("raw_event.not_found", raw_event_id=raw_event_id)
        return

    if raw_event.status == EventStatus.PROCESSED:
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

        # Update raw_event status
        raw_event.status = EventStatus.FAILED
        raw_event.processed_at = datetime.utcnow()

        await session.commit()

        logger.error(
            "raw_event.processing_failed",
            raw_event_id=raw_event.id,
            handler=handler_name,
            error=str(e),
        )
