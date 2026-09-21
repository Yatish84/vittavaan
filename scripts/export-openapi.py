"""Regenerate the committed OpenAPI contract deterministically."""

import json
from pathlib import Path

from vittavaan.boundary.api import create_app
from vittavaan.config import Settings

settings = Settings(
    APP_ENV="test",
    APP_RELEASE_ID="contract-generation",
    DATABASE_URL="postgresql+asyncpg://user:secret@localhost/test",
    REDIS_URL="redis://:secret@localhost:6379/0",
)
contract = json.dumps(create_app(settings).openapi(), sort_keys=True, separators=(",", ":"))
target = Path("packages/contracts/openapi.json")
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(contract + "\n", encoding="utf-8")
print(f"Wrote deterministic contract to {target}")
