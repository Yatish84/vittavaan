"""Cache readiness and bounded queue monitoring without a network dependency."""

import json
from datetime import UTC, datetime, timedelta
from typing import cast

import pytest
from redis.asyncio import Redis
from vittavaan.infrastructure.cache import cache_ready, worker_queue_status


class HealthyCache:
    async def ping(self) -> bool:
        return True


class UnavailableCache:
    async def ping(self) -> bool:
        raise ConnectionError("synthetic unavailable cache")


class QueueCache:
    def __init__(self, messages: list[str]) -> None:
        self.messages = messages

    async def llen(self, _queue_name: str) -> int:
        return len(self.messages)

    async def lindex(self, _queue_name: str, index: int) -> str | None:
        return self.messages[index] if self.messages else None


@pytest.mark.asyncio
async def test_cache_readiness_reports_success_and_failure() -> None:
    assert await cache_ready(cast(Redis, HealthyCache()))
    assert not await cache_ready(cast(Redis, UnavailableCache()))


@pytest.mark.asyncio
async def test_queue_status_reports_only_depth_and_oldest_age() -> None:
    enqueued_at = datetime.now(UTC) - timedelta(seconds=2)
    message = json.dumps(
        {
            "headers": {"vittavaan_enqueued_at": enqueued_at.isoformat()},
            "body": "must-not-be-returned",
        }
    )
    depth, age = await worker_queue_status(cast(Redis, QueueCache([message])))

    assert depth == 1
    assert 1 <= age <= 4


@pytest.mark.asyncio
async def test_queue_status_tolerates_missing_or_malformed_timestamp() -> None:
    depth, age = await worker_queue_status(cast(Redis, QueueCache(["not-json"])))
    assert (depth, age) == (1, 0.0)
