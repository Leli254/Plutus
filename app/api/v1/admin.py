from fastapi import APIRouter

router = APIRouter(prefix="/admin")


@router.get("/stats")
def system_stats():
    return {
        "message": "Operational metrics placeholder"
    }
