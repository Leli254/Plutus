import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.ingestion.idempotency import (
    get_or_create_raw_event, IdempotencyResult
    )
from app.ingestion.schemas import IngestRequest
from app.core.logging import get_logger
from app.observability.tracing import get_tracer

logger = get_logger("ingestion.service")
tracer = get_tracer()


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

    # ---- TRACE SPAN START ----
    with tracer.start_as_current_span("ingest_event") as span:
        # Attach high-cardinality-safe attributes
        span.set_attribute("event.source", payload.source)
        span.set_attribute(
            "event.idempotency_key_present",
            payload.idempotency_key is not None,
        )
        span.set_attribute("event.schema_version", payload.schema_version)

        try:
            result: IdempotencyResult = await get_or_create_raw_event(
                session=session,
                source=payload.source,
                payload=payload.dict(),
                schema_version=payload.schema_version,
                idempotency_key=payload.idempotency_key,
            )

            span.set_attribute("event.id", str(result.event.id))
            span.set_attribute("event.created", result.created)

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

            return result.event.id

        except Exception as e:
            # Record exception on the trace
            span.record_exception(e)
            span.set_attribute("event.ingest_failed", True)

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
