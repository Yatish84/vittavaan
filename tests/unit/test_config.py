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
            DATABASE_URL="postgresql+asyncpg://user:secret@db/app",
            REDIS_URL="redis://:secret@cache:6379/0",
        )
