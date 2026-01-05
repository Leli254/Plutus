import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings, Settings
from app.core.logging import configure_logging, get_logger

from app.api.v1.router import router as api_v1_router

logger = get_logger("main")

settings: Settings = get_settings()


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    # Configure logging
    configure_logging()
    logger.info("Starting application", environment=settings.environment)

    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        debug=settings.debug,
    )

    # CORS (optional, adjust for production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API v1 routes
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    # Startup event
    @app.on_event("startup")
    async def on_startup():
        logger.info("Application startup complete")

    # Shutdown event
    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("Application shutdown complete")

    return app


app = create_app()

if __name__ == "__main__":
    # For local development
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
