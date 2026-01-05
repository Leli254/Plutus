from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db_session
from app.processing.service import process_raw_event
from app.db.models.raw_event import RawEvent

router = APIRouter(prefix="/processing", tags=["processing"])


@router.post("/manual/{raw_event_id}")
async def manual_process_event(
    raw_event_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Trigger processing of a RawEvent manually by ID.
    """
    try:
        await process_raw_event(raw_event_id, session, handler_name="manual_trigger")
        return {"status": "success", "raw_event_id": raw_event_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/pending", response_model=List[str])
async def list_pending_events(session: AsyncSession = Depends(get_db_session)):
    """
    List all pending RawEvents (not yet processed).
    """
    result = await session.execute(
        RawEvent.__table__.select().where(RawEvent.status == "RECEIVED")
    )
    pending_events = [str(row.id) for row in result.fetchall()]
    return pending_events
