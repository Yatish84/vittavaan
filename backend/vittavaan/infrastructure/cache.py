"""Valkey/Redis connectivity owned by the infrastructure layer."""

import json
from collections.abc import Awaitable
from datetime import UTC, datetime
from typing import cast

from redis import Redis as SyncRedis
from redis.asyncio import Redis

WORKER_METRICS_KEY = "vittavaan:metrics:worker:v1"


def create_cache(redis_url: str) -> Redis:
    """Create a decoded Redis-protocol client with bounded socket timeouts."""

    return cast(
        Redis,
        Redis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
            health_check_interval=15,
        ),
    )


async def cache_ready(client: Redis) -> bool:
    """Return whether the required cache/broker service responds safely."""

    try:
        return bool(await client.ping())
    except Exception:
        return False


async def worker_queue_status(client: Redis, queue_name: str = "celery") -> tuple[int, float]:
    """Return aggregate queue depth/oldest age without reading task arguments."""

    depth = int(await cast(Awaitable[int], client.llen(queue_name)))
    if depth == 0:
        return 0, 0.0
    oldest_message = await cast(Awaitable[str | None], client.lindex(queue_name, -1))
    if not oldest_message:
        return depth, 0.0
    try:
        envelope = json.loads(oldest_message)
        raw_timestamp = envelope.get("headers", {}).get("vittavaan_enqueued_at")
        enqueued_at = datetime.fromisoformat(str(raw_timestamp))
        if enqueued_at.tzinfo is None:
            return depth, 0.0
        age = (datetime.now(UTC) - enqueued_at.astimezone(UTC)).total_seconds()
        return depth, max(0.0, age)
    except (AttributeError, TypeError, ValueError, json.JSONDecodeError):
        return depth, 0.0


def increment_worker_metrics(redis_url: str, increments: dict[str, int]) -> None:
    """Atomically store bounded worker aggregates for cross-process scraping."""

    client = SyncRedis.from_url(
        redis_url, socket_connect_timeout=2, socket_timeout=2, decode_responses=True
    )
    try:
        pipeline = client.pipeline(transaction=True)
        for field, amount in increments.items():
            pipeline.hincrby(WORKER_METRICS_KEY, field, amount)
        pipeline.expire(WORKER_METRICS_KEY, 86400)
        pipeline.execute()
    finally:
        client.close()


async def worker_metric_snapshot(client: Redis) -> dict[str, int]:
    """Read aggregate worker metrics without task payloads or identifiers."""

    raw = await cast(Awaitable[dict[str, str]], client.hgetall(WORKER_METRICS_KEY))
    return {field: int(value) for field, value in raw.items()}
