import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.ingestion.idempotency import get_or_create_raw_event, IdempotencyResult
from app.ingestion.schemas import IngestRequest
from app.core.logging import get_logger

logger = get_logger("ingestion.service")


async def ingest_event(payload: IngestRequest, session: AsyncSession) -> uuid.UUID:
    """
    Ingest a single webhook payload.

    Steps:
    1. Enforce idempotency via database constraint
    2. Persist raw event (immutable)
    3. Return event ID for async processing / queue publishing

    Raises:
        HTTPException if persistence fails
    """

    try:
        result: IdempotencyResult = await get_or_create_raw_event(
            session=session,
            source=payload.source,
            payload=payload.dict(),
            schema_version=payload.schema_version,
            idempotency_key=payload.idempotency_key,
        )

        if result.created:
            logger.info(
                "raw_event.created",
                event_id=str(result.event.id),
                source=payload.source,
                idempotency_key=payload.idempotency_key,
            )
        else:
            logger.info(
                "raw_event.duplicate",
                event_id=str(result.event.id),
                source=payload.source,
                idempotency_key=payload.idempotency_key,
            )

        # Caller can publish to queue after this
        return result.event.id

    except Exception as e:
        logger.error(
            "raw_event.ingest_failed",
            error=str(e),
            source=payload.source,
            idempotency_key=payload.idempotency_key,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to ingest event",
        )
