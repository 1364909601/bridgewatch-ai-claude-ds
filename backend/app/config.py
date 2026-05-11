from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "BridgeWatch AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/bridgewatch"
    DATABASE_SYNC_URL: Optional[str] = None  # For Alembic sync operations, derived if not set

    # JWT
    SECRET_KEY: str = "bridgewatch-dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # File storage
    FILE_STORAGE_PATH: str = "./data/files"
    FILE_SERVE_URL: str = "/files"  # Nginx or backend static file serving prefix

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_SYNC_URL:
            return self.DATABASE_SYNC_URL
        # Derive sync URL from async URL
        return self.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

    # Inference Worker
    WORKER_ENABLED: bool = True
    WORKER_POLL_INTERVAL: int = 5

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
