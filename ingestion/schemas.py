from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime
import uuid


class IngestRequest(BaseModel):
    """
    Schema for incoming webhook or ingestion payload.
    """

    source: str = Field(
        ...,
        description="Origin of the event (e.g., 'webhook', 'partner_name')",
        max_length=100,
        example="webhook",
    )
    idempotency_key: str = Field(
        ...,
        description="Unique key to ensure idempotent processing",
        max_length=255,
        example="abc123-unique-key",
    )
    schema_version: str = Field(
        ...,
        description="Version of the event payload schema",
        max_length=20,
        example="1.0",
    )
    payload: Dict[str, Any] = Field(
        ...,
        description="Event payload data",
        example={"order_id": 123, "status": "paid"},
    )
    received_at: datetime | None = Field(
        None,
        description="Optional timestamp of when the event was created at source",
        example="2026-01-05T17:00:00Z",
    )


class IngestResponse(BaseModel):
    """
    Response schema for ingestion endpoints.
    """

    event_id: uuid.UUID = Field(
        ...,
        description="The database ID of the ingested raw event",
        example="9a8b7c6d-5e4f-1234-5678-90abcdef1234",
    )
