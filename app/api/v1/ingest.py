from fastapi import APIRouter, Depends, status

from app.core.security import api_key_auth
from app.ingestion.schemas import IngestRequest, IngestResponse
from app.ingestion.service import ingest_event

router = APIRouter(
    prefix="/ingest",
    dependencies=[Depends(api_key_auth)],
)


@router.post(
    "/webhook",
    response_model=IngestResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def ingest_webhook(payload: IngestRequest):
    event_id = await ingest_event(payload)
    return IngestResponse(event_id=event_id)
