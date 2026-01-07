import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from db.enums import EventStatus


class RawEvent(Base):
    __tablename__ = "raw_events"
    __table_args__ = (
        UniqueConstraint(
            "source",
            "idempotency_key",
            name="uq_raw_event_idempotency",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    payload: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    schema_version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    idempotency_key: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus, name="event_status"),
        nullable=False,
        default=EventStatus.RECEIVED,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
