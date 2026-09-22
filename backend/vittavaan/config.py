"""Typed runtime configuration with file-based secret support."""

from functools import lru_cache
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit

from pydantic import AnyHttpUrl, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated non-secret configuration and secret file references."""

    model_config = SettingsConfigDict(env_file=".env", extra="forbid", case_sensitive=True)

    APP_ENV: Literal["local", "test", "staging", "production"] = "local"
    APP_RELEASE_ID: str = "development"
    PUBLIC_WEB_URL: AnyHttpUrl = AnyHttpUrl("http://localhost:5173")
    PUBLIC_API_URL: AnyHttpUrl = AnyHttpUrl("http://localhost:8000/api/v1")
    AUTH_CORE_WEB_URL: AnyHttpUrl = AnyHttpUrl("http://localhost:3000")
    AUTH_CORE_API_URL: AnyHttpUrl = AnyHttpUrl("http://localhost:8001")
    AUTH_CORE_VERIFIER_URL: AnyHttpUrl = AnyHttpUrl("http://localhost:8081")
    AUTH_RETURN_URL: AnyHttpUrl = AnyHttpUrl("http://localhost:5173/auth/return")
    AUTH_VERIFIER_TIMEOUT_SECONDS: float = Field(default=2.0, ge=0.1, le=10.0)
    AUTH_ALLOWED_CLIENT_TYPES: frozenset[str] = frozenset({"WEB"})
    AUTH_CORE_HANDOFF_CLIENT_SECRET: str | None = Field(default=None, repr=False)
    AUTH_CORE_HANDOFF_CLIENT_SECRET_FILE: Path | None = None
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
        if self.AUTH_CORE_HANDOFF_CLIENT_SECRET and self.AUTH_CORE_HANDOFF_CLIENT_SECRET_FILE:
            raise ValueError(
                "Set only AUTH_CORE_HANDOFF_CLIENT_SECRET or "
                "AUTH_CORE_HANDOFF_CLIENT_SECRET_FILE, not both"
            )
        if self.AUTH_CORE_HANDOFF_CLIENT_SECRET_FILE:
            try:
                self.AUTH_CORE_HANDOFF_CLIENT_SECRET = (
                    self.AUTH_CORE_HANDOFF_CLIENT_SECRET_FILE.read_text(encoding="utf-8").strip()
                )
            except OSError as exc:
                raise ValueError("Unable to read AUTH_CORE_HANDOFF_CLIENT_SECRET_FILE") from exc
        if not self.AUTH_CORE_HANDOFF_CLIENT_SECRET and self.APP_ENV in {"local", "test"}:
            self.AUTH_CORE_HANDOFF_CLIENT_SECRET = "local-handoff-client-secret-change-me"
        if not self.AUTH_CORE_HANDOFF_CLIENT_SECRET or len(
            self.AUTH_CORE_HANDOFF_CLIENT_SECRET
        ) < 32:
            raise ValueError("AUTH_CORE_HANDOFF_CLIENT_SECRET must contain at least 32 characters")
        if self.APP_ENV in {"staging", "production"} and self.APP_RELEASE_ID == "development":
            raise ValueError("A real APP_RELEASE_ID is required outside local/test")
        if self.APP_ENV in {"staging", "production"}:
            if (
                self.AUTH_CORE_HANDOFF_CLIENT_SECRET
                == "local-handoff-client-secret-change-me"
            ):
                raise ValueError("The local handoff secret cannot be used outside local/test")
            if urlsplit(str(self.PUBLIC_WEB_URL)).scheme != "https":
                raise ValueError("PUBLIC_WEB_URL must use HTTPS outside local/test")
            if urlsplit(str(self.AUTH_CORE_WEB_URL)).scheme != "https":
                raise ValueError("AUTH_CORE_WEB_URL must use HTTPS outside local/test")
            if urlsplit(str(self.AUTH_RETURN_URL)).scheme != "https":
                raise ValueError("AUTH_RETURN_URL must use HTTPS outside local/test")
        if not self.AUTH_ALLOWED_CLIENT_TYPES or any(
            not value.strip() for value in self.AUTH_ALLOWED_CLIENT_TYPES
        ):
            raise ValueError("AUTH_ALLOWED_CLIENT_TYPES must contain non-empty values")
        public_origin = urlsplit(str(self.PUBLIC_WEB_URL))
        return_origin = urlsplit(str(self.AUTH_RETURN_URL))
        if (public_origin.scheme, public_origin.netloc) != (
            return_origin.scheme,
            return_origin.netloc,
        ):
            raise ValueError("AUTH_RETURN_URL must use the PUBLIC_WEB_URL origin")
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide immutable settings instance."""

    return Settings()
