"""Contract checks for Vittavaan's foundation-only OpenAPI document."""

import hashlib
import json
from pathlib import Path

from vittavaan.boundary.api import create_app
from vittavaan.config import Settings

CONTRACT_PATH = Path("packages/contracts/openapi.json")


def test_openapi_is_deterministic_and_matches_committed_contract() -> None:
    settings = Settings(
        APP_ENV="test",
        APP_RELEASE_ID="contract-test",
        DATABASE_URL="postgresql+asyncpg://user:secret@localhost/test",
        REDIS_URL="redis://:secret@localhost:6379/0",
    )
    first = json.dumps(create_app(settings).openapi(), sort_keys=True, separators=(",", ":"))
    second = json.dumps(create_app(settings).openapi(), sort_keys=True, separators=(",", ":"))
    committed = CONTRACT_PATH.read_text(encoding="utf-8").strip()

    assert first == second
    assert first == committed
    assert set(json.loads(first)["paths"]) == {
        "/api/v1/bootstrap",
        "/api/v1/auth/handoff/exchange",
        "/api/v1/auth/handoff/start",
        "/health/live",
        "/health/ready",
    }
    assert (
        hashlib.sha256(first.encode()).hexdigest() == hashlib.sha256(committed.encode()).hexdigest()
    )
