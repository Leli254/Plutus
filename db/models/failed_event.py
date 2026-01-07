import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class FailedEvent(Base):
    __tablename__ = "failed_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    raw_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("raw_events.id", ondelete="CASCADE"),
        nullable=False,
    )

    error_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    error_message: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    failed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    raw_event = relationship("RawEvent", lazy="joined")
