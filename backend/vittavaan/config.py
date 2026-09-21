"""Typed runtime configuration with file-based secret support."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import AnyHttpUrl, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated non-secret configuration and secret file references."""

    model_config = SettingsConfigDict(env_file=".env", extra="forbid", case_sensitive=True)

    APP_ENV: Literal["local", "test", "staging", "production"] = "local"
    APP_RELEASE_ID: str = "development"
    PUBLIC_WEB_URL: AnyHttpUrl = AnyHttpUrl("http://localhost:5173")
    PUBLIC_API_URL: AnyHttpUrl = AnyHttpUrl("http://localhost:8000/api/v1")
    DATABASE_URL: str | None = Field(default=None, repr=False)
    DATABASE_URL_FILE: Path | None = None
    REDIS_URL: str | None = Field(default=None, repr=False)
    REDIS_URL_FILE: Path | None = None
    WORKER_VISIBILITY_TIMEOUT_SECONDS: int = Field(default=3600, ge=5, le=86400)
    OTEL_EXPORTER_ENDPOINT: str | None = None

    @staticmethod
    def _read_secret(value: str | None, file_path: Path | None, name: str) -> str:
        if value and file_path:
            raise ValueError(f"Set only {name} or {name}_FILE, not both")
        if file_path:
            try:
                return file_path.read_text(encoding="utf-8").strip()
            except OSError as exc:
                raise ValueError(f"Unable to read {name}_FILE") from exc
        if value:
            return value
        raise ValueError(f"Missing {name} or {name}_FILE")

    @model_validator(mode="after")
    def resolve_secrets(self) -> "Settings":
        self.DATABASE_URL = self._read_secret(
            self.DATABASE_URL, self.DATABASE_URL_FILE, "DATABASE_URL"
        )
        self.REDIS_URL = self._read_secret(self.REDIS_URL, self.REDIS_URL_FILE, "REDIS_URL")
        if self.APP_ENV in {"staging", "production"} and self.APP_RELEASE_ID == "development":
            raise ValueError("A real APP_RELEASE_ID is required outside local/test")
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide immutable settings instance."""

    return Settings()
