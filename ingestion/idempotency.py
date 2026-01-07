import uuid
from typing import Tuple

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.raw_event import RawEvent
from db.enums import EventStatus


class IdempotencyResult:
    """
    Result object to make intent explicit at call sites.
    """

    def __init__(self, event: RawEvent, created: bool):
        self.event = event
        self.created = created


async def get_or_create_raw_event(
    *,
    session: AsyncSession,
    source: str,
    payload: dict,
    schema_version: str,
    idempotency_key: str,
) -> IdempotencyResult:
    """
    Create a RawEvent if it does not already exist.

    Guarantees:
    - Safe under concurrent requests
    - No duplicate rows
    - Exactly one RawEvent per (source, idempotency_key)

    Strategy:
    1. Attempt INSERT
    2. If UNIQUE violation occurs, SELECT existing row
    """

    raw_event = RawEvent(
        id=uuid.uuid4(),
        source=source,
        payload=payload,
        schema_version=schema_version,
        idempotency_key=idempotency_key,
        status=EventStatus.RECEIVED,
    )

    session.add(raw_event)

    try:
        await session.flush()
        # Flush succeeded → row was created
        return IdempotencyResult(event=raw_event, created=True)

    except IntegrityError:
        # Another request already inserted this event
        await session.rollback()

        result = await session.execute(
            select(RawEvent).where(
                RawEvent.source == source,
                RawEvent.idempotency_key == idempotency_key,
            )
        )

        existing_event = result.scalar_one()

        return IdempotencyResult(event=existing_event, created=False)
