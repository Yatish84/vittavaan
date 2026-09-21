"""Worker reliability configuration and safe task instrumentation tests."""

import importlib
from types import ModuleType

import pytest
from vittavaan.config import get_settings


@pytest.fixture
def worker_module(monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("APP_RELEASE_ID", "worker-test")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://user:secret@localhost/test")
    monkeypatch.setenv("REDIS_URL", "redis://:secret@localhost:6379/0")
    get_settings.cache_clear()
    module = importlib.import_module("vittavaan.boundary.worker")
    monkeypatch.setattr(module, "increment_worker_metrics", lambda *_args, **_kwargs: None)
    yield module
    get_settings.cache_clear()


def test_worker_has_bounded_failure_and_delivery_settings(worker_module: ModuleType) -> None:
    configuration = worker_module.celery_app.conf
    assert configuration.task_acks_late is True
    assert configuration.task_reject_on_worker_lost is True
    assert configuration.worker_prefetch_multiplier == 1
    assert configuration.broker_connection_max_retries == 12
    assert configuration.task_soft_time_limit == 60
    assert configuration.task_time_limit == 90
    assert configuration.broker_transport_options["visibility_timeout"] == 3600
    assert configuration.result_backend_transport_options["visibility_timeout"] == 3600
    assert configuration.visibility_timeout == 3600


def test_smoke_task_is_deterministic(worker_module: ModuleType) -> None:
    correlation_id = "11111111-1111-4111-8111-111111111111"
    expected = {"status": "ok", "correlation_id": correlation_id}
    assert worker_module.smoke_task.run(correlation_id) == expected
    assert worker_module.smoke_task.run(correlation_id) == expected


def test_worker_timing_state_is_removed_after_completion(worker_module: ModuleType) -> None:
    task_id = "synthetic-task-id"
    worker_module.record_task_start(task_id=task_id, task=worker_module.smoke_task)
    assert task_id in worker_module.task_started_at

    worker_module.record_task_finish(
        task_id=task_id,
        task=worker_module.smoke_task,
        state="SUCCESS",
    )
    assert task_id not in worker_module.task_started_at
    output = worker_module.worker_metrics.render_prometheus()
    assert 'task_name="foundation.smoke.v1",state="SUCCESS"' in output


def test_publish_signal_adds_only_a_technical_timestamp(worker_module: ModuleType) -> None:
    headers: dict[str, object] = {"existing": "safe"}
    worker_module.record_enqueue_time(headers=headers)

    assert headers["existing"] == "safe"
    assert "vittavaan_enqueued_at" in headers


def test_recovery_probe_is_bounded(
    worker_module: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    slept_for: list[int] = []
    monkeypatch.setattr(worker_module, "sleep", slept_for.append)
    correlation_id = "22222222-2222-4222-8222-222222222222"

    result = worker_module.recovery_probe_task.run(correlation_id, 1000)

    assert slept_for == [45]
    assert result == {"status": "recovered", "correlation_id": correlation_id}
