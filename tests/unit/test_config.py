from pathlib import Path

import pytest
from vittavaan.config import Settings


def test_reads_secrets_from_files(tmp_path: Path) -> None:
    database = tmp_path / "database"
    redis = tmp_path / "redis"
    database.write_text("postgresql+asyncpg://user:secret@db/app", encoding="utf-8")
    redis.write_text("redis://:secret@cache:6379/0", encoding="utf-8")

    settings = Settings(DATABASE_URL_FILE=database, REDIS_URL_FILE=redis)

    assert settings.DATABASE_URL.startswith("postgresql+asyncpg://")
    assert settings.REDIS_URL.startswith("redis://")


def test_rejects_development_release_in_staging() -> None:
    with pytest.raises(ValueError, match="APP_RELEASE_ID"):
        Settings(
            APP_ENV="staging",
            AUTH_CORE_HANDOFF_CLIENT_SECRET="staging-secret-with-at-least-32-characters",
            DATABASE_URL="postgresql+asyncpg://user:secret@db/app",
            REDIS_URL="redis://:secret@cache:6379/0",
        )


def test_rejects_local_handoff_secret_outside_local_test() -> None:
    with pytest.raises(ValueError, match="local handoff secret"):
        Settings(
            APP_ENV="staging",
            APP_RELEASE_ID="release-1",
            PUBLIC_WEB_URL="https://wealth.example.test",
            AUTH_CORE_WEB_URL="https://auth.example.test",
            AUTH_RETURN_URL="https://wealth.example.test/auth/return",
            DATABASE_URL="postgresql+asyncpg://user:secret@db/app",
            REDIS_URL="redis://:secret@cache:6379/0",
            AUTH_CORE_HANDOFF_CLIENT_SECRET="local-handoff-client-secret-change-me",
        )


def test_rejects_auth_return_url_on_another_origin() -> None:
    with pytest.raises(ValueError, match="AUTH_RETURN_URL"):
        Settings(
            AUTH_RETURN_URL="https://attacker.example/return",
            DATABASE_URL="postgresql+asyncpg://user:secret@db/app",
            REDIS_URL="redis://:secret@cache:6379/0",
        )


def test_auth_configuration_is_bounded() -> None:
    settings = Settings(
        AUTH_VERIFIER_TIMEOUT_SECONDS=1.5,
        AUTH_ALLOWED_CLIENT_TYPES=frozenset({"WEB"}),
        DATABASE_URL="postgresql+asyncpg://user:secret@db/app",
        REDIS_URL="redis://:secret@cache:6379/0",
    )

    assert settings.AUTH_VERIFIER_TIMEOUT_SECONDS == 1.5
    assert frozenset({"WEB"}) == settings.AUTH_ALLOWED_CLIENT_TYPES
