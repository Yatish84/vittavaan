"""Real local-service checks using isolated synthetic keys only."""

import asyncio
import json
import os
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import httpx
import pytest
from boto3 import client as boto3_client
from botocore.config import Config
from celery import Celery  # type: ignore[import-untyped]
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from vittavaan.infrastructure.cache import cache_ready, create_cache, worker_queue_status
from vittavaan.infrastructure.database import (
    FOUNDATION_SCHEMA_HEAD,
    create_engine,
    database_ready,
)

pytestmark = pytest.mark.integration


def required_environment(name: str) -> str:
    value = os.getenv(name)
    if not value:
        pytest.skip(f"{name} is required for integration tests")
    return value


def required_secret_file(name: str) -> str:
    path = required_environment(name)
    with open(path, encoding="utf-8") as secret_file:
        return secret_file.read().strip()


@pytest.mark.asyncio
async def test_postgres_is_current_and_migration_is_repeatable() -> None:
    database_url = required_environment("VITTAVAAN_INTEGRATION_DATABASE_URL")
    migration_database_url = required_environment("VITTAVAAN_INTEGRATION_MIGRATION_DATABASE_URL")
    redis_url = required_environment("VITTAVAAN_INTEGRATION_REDIS_URL")
    migration_environment = {
        **os.environ,
        "DATABASE_URL": migration_database_url,
        "REDIS_URL": redis_url,
        "APP_ENV": "test",
        "APP_RELEASE_ID": "integration-test",
        "PYTHONPATH": "backend",
    }

    first_process = await asyncio.create_subprocess_exec(
        "uv",
        "run",
        "alembic",
        "upgrade",
        "head",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=migration_environment,
    )
    second_process = await asyncio.create_subprocess_exec(
        "uv",
        "run",
        "alembic",
        "upgrade",
        "head",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=migration_environment,
    )
    (first_stdout, first_stderr), (second_stdout, second_stderr) = await asyncio.gather(
        first_process.communicate(), second_process.communicate()
    )
    assert first_process.returncode == 0, (first_stdout + first_stderr).decode()
    assert second_process.returncode == 0, (second_stdout + second_stderr).decode()

    engine = create_engine(database_url)
    try:
        assert await database_ready(engine)
        assert not await database_ready(engine, expected_head="deliberately-wrong-head")
        async with engine.connect() as connection:
            head = await connection.scalar(text("SELECT version_num FROM alembic_version"))
        assert head == FOUNDATION_SCHEMA_HEAD
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_application_role_cannot_modify_database_structure() -> None:
    database_url = required_environment("VITTAVAAN_INTEGRATION_DATABASE_URL")
    migration_database_url = required_environment("VITTAVAAN_INTEGRATION_MIGRATION_DATABASE_URL")
    app_engine = create_engine(database_url)
    migration_engine = create_engine(migration_database_url)
    try:
        async with app_engine.connect() as connection:
            app_can_create = await connection.scalar(
                text("SELECT has_schema_privilege(current_user, 'public', 'CREATE')")
            )
            assert app_can_create is False
            with pytest.raises(DBAPIError):
                await connection.execute(text("CREATE TABLE forbidden_app_table (id integer)"))

        async with migration_engine.connect() as connection:
            migrator_can_create = await connection.scalar(
                text("SELECT has_schema_privilege(current_user, 'public', 'CREATE')")
            )
            assert migrator_can_create is True
    finally:
        await app_engine.dispose()
        await migration_engine.dispose()


@pytest.mark.asyncio
async def test_valkey_round_trip_uses_and_removes_an_isolated_key() -> None:
    redis_url = required_environment("VITTAVAAN_INTEGRATION_REDIS_URL")
    client = create_cache(redis_url)
    key = f"vittavaan:integration:{uuid4()}"
    try:
        assert await client.ping()
        assert await cache_ready(client)
        assert await client.set(key, "synthetic", ex=30, nx=True)
        assert await client.get(key) == "synthetic"
    finally:
        await client.delete(key)
        await client.aclose()


@pytest.mark.asyncio
async def test_capacity_metrics_use_aggregate_values_only() -> None:
    redis_url = required_environment("VITTAVAAN_INTEGRATION_REDIS_URL")
    client = create_cache(redis_url)
    queue_name = f"vittavaan:integration:queue:{uuid4()}"
    marker = str(uuid4())
    message = json.dumps(
        {
            "headers": {
                "vittavaan_enqueued_at": (datetime.now(UTC) - timedelta(seconds=1)).isoformat()
            },
            "body": marker,
        }
    )
    try:
        await client.rpush(queue_name, message)
        depth, oldest_age = await worker_queue_status(client, queue_name)
        assert depth == 1
        assert oldest_age >= 0.5

        async with httpx.AsyncClient(base_url="http://api:8000") as http_client:
            readiness = await http_client.get("/health/ready")
            metrics = await http_client.get("/metrics")
        assert readiness.status_code == 200
        assert 'vittavaan_database_pool_connections{state="size"} 5' in metrics.text
        assert "vittavaan_worker_queue_depth" in metrics.text
        assert marker not in metrics.text
    finally:
        await client.delete(queue_name)
        await client.aclose()


def test_s3_compatible_object_round_trip_cleans_up() -> None:
    endpoint = required_environment("VITTAVAAN_INTEGRATION_OBJECT_ENDPOINT")
    access_key = required_secret_file("VITTAVAAN_INTEGRATION_OBJECT_ACCESS_KEY_FILE")
    secret_key = required_secret_file("VITTAVAAN_INTEGRATION_OBJECT_SECRET_KEY_FILE")
    bucket = f"vittavaan-integration-{uuid4()}"
    object_key = f"synthetic/{uuid4()}.txt"
    payload = b"synthetic object integration probe"
    s3 = boto3_client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="us-east-1",
        config=Config(s3={"addressing_style": "path"}),
    )
    try:
        s3.create_bucket(Bucket=bucket)
        s3.put_object(Bucket=bucket, Key=object_key, Body=payload)
        response = s3.get_object(Bucket=bucket, Key=object_key)
        assert response["Body"].read() == payload
    finally:
        try:
            s3.delete_object(Bucket=bucket, Key=object_key)
            s3.delete_bucket(Bucket=bucket)
        finally:
            s3.close()


def test_worker_completes_duplicate_synthetic_tasks_without_durable_side_effects() -> None:
    redis_url = required_environment("VITTAVAAN_INTEGRATION_REDIS_URL")
    correlation_id = str(uuid4())
    client = Celery("integration-client", broker=redis_url, backend=redis_url)
    headers = {
        "vittavaan_correlation_id": correlation_id,
        "vittavaan_causation_id": correlation_id,
    }
    first = client.send_task("foundation.smoke.v1", args=[correlation_id], headers=headers)
    second = client.send_task("foundation.smoke.v1", args=[correlation_id], headers=headers)

    expected = {"status": "ok", "correlation_id": correlation_id}
    assert first.get(timeout=15) == expected
    assert second.get(timeout=15) == expected

    metrics = httpx.get("http://api:8000/metrics", timeout=5)
    assert metrics.status_code == 200
    total_line = next(
        line
        for line in metrics.text.splitlines()
        if line.startswith(
            'vittavaan_worker_tasks_total{task_name="foundation.smoke.v1",state="SUCCESS"}'
        )
    )
    assert int(total_line.rsplit(" ", 1)[1]) >= 2
    assert 'vittavaan_worker_task_duration_seconds_bucket{task_name="foundation.smoke.v1"' in (
        metrics.text
    )
    assert correlation_id not in metrics.text

    first.forget()
    second.forget()
