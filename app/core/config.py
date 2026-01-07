from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================
    # Application
    # =========================
    app_name: str = "Ingestor"
    environment: str = Field(default="development")
    debug: bool = Field(default=False)

    # =========================
    # API
    # =========================
    api_v1_prefix: str = "/api/v1"

    # =========================
    # Database
    # =========================
    database_url: str = Field(
        description="PostgreSQL DSN",
        examples=["postgresql+asyncpg://user:pass@localhost:5432/ingestor"],
    )

    # =========================
    # Redis
    # =========================
    redis_url: str = Field(default="redis://localhost:6379/0")

    # =========================
    # Observability
    # =========================
    log_level: str = Field(default="INFO")

    metrics_enabled: bool = Field(
        default=True,
        description="Enable Prometheus metrics",
    )

    tracing_enabled: bool = Field(
        default=True,
        description="Enable OpenTelemetry tracing",
    )

    service_name: str = Field(
        default="ingestor",
        description="Logical service name for metrics/tracing",
    )

    otlp_endpoint: str | None = Field(
        default=None,
        description="OTLP gRPC endpoint, e.g. http://otel-collector:4317",
    )

    # =========================
    # Pydantic config
    # =========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    Ensures settings are loaded once per process.
    """
    return Settings()
