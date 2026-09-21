"""Alembic environment for Vittavaan migrations."""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from vittavaan.config import get_settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None


MIGRATION_ADVISORY_LOCK_ID = 8_675_309


def do_run_migrations(connection: Connection) -> None:
    """Run migrations while holding the Vittavaan deployment advisory lock."""

    connection.execute(
        text("SELECT pg_advisory_lock(:lock_id)"), {"lock_id": MIGRATION_ADVISORY_LOCK_ID}
    )
    # SQLAlchemy begins a transaction for the lock query. Commit that transaction
    # before Alembic opens its migration transaction; PostgreSQL session-level
    # advisory locks remain held across commits.
    connection.commit()
    try:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.execute(
            text("SELECT pg_advisory_unlock(:lock_id)"),
            {"lock_id": MIGRATION_ADVISORY_LOCK_ID},
        )
        connection.commit()


async def run_async_migrations() -> None:
    """Create an async migration connection from validated settings."""

    section = config.get_section(config.config_ini_section, {})
    section["sqlalchemy.url"] = str(get_settings().DATABASE_URL)
    connectable = async_engine_from_config(section, prefix="sqlalchemy.", poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    raise RuntimeError("Offline SQL generation is not enabled until migration policy supports it")
asyncio.run(run_async_migrations())
