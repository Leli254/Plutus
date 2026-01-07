# main.py

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings, Settings
from app.core.logging import configure_logging, get_logger
from app.api.v1.router import router as api_v1_router

from observability.metrics import setup_prometheus
from observability.tracing import setup_tracing

logger = get_logger("main")
settings: Settings = get_settings()


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    # Configure structured logging
    configure_logging()
    logger.info(
        "Starting application",
        environment=settings.environment,
        debug=settings.debug,
    )

    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        debug=settings.debug,
    )

    # -----------------------------
    # Middleware
    # -----------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -----------------------------
    # Routes
    # -----------------------------
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    # -----------------------------
    # Observability
    # -----------------------------
    setup_prometheus(app)
    setup_tracing(
        app,
        service_name=settings.app_name,
    )

    # -----------------------------
    # Lifecycle hooks
    # -----------------------------
    @app.on_event("startup")
    async def on_startup() -> None:
        logger.info("Application startup complete")

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        logger.info("Application shutdown complete")

    return app


app = create_app()


def run_api() -> None:
    """
    Entrypoint for: poetry run start-api
    """
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    run_api()
