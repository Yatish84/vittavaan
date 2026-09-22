"""Async PostgreSQL connectivity owned by the infrastructure layer."""

from collections.abc import AsyncIterator
from typing import cast

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

FOUNDATION_SCHEMA_HEAD = "20260921_0002"


def create_engine(database_url: str) -> AsyncEngine:
    """Create a bounded async database engine."""

    return create_async_engine(database_url, pool_pre_ping=True, pool_size=5, max_overflow=5)


def database_pool_status(engine: AsyncEngine) -> dict[str, int]:
    """Return aggregate pool capacity without exposing connection information."""

    pool = engine.pool
    size = getattr(pool, "size", lambda: 0)()
    checked_out = getattr(pool, "checkedout", lambda: 0)()
    overflow = getattr(pool, "overflow", lambda: 0)()
    return {
        "size": max(0, int(size)),
        "checked_out": max(0, int(checked_out)),
        "overflow": max(0, int(overflow)),
    }


async def database_ready(engine: AsyncEngine, expected_head: str = FOUNDATION_SCHEMA_HEAD) -> bool:
    """Return whether PostgreSQL is reachable and at the expected migration head."""

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
            current_head = cast(
                str | None,
                await connection.scalar(text("SELECT version_num FROM alembic_version")),
            )
        return current_head == expected_head
    except Exception:
        return False


async def dispose_engine(engine: AsyncEngine) -> AsyncIterator[None]:
    """Dispose the database engine in an async lifecycle."""

    try:
        yield
    finally:
        await engine.dispose()
