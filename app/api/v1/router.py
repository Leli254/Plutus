from fastapi import APIRouter

from app.api.v1 import health, ingest

router = APIRouter()

router.include_router(health.router, tags=["health"])
router.include_router(ingest.router, tags=["ingestion"])
