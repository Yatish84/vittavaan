"""Celery worker foundation with bounded failure behavior and safe telemetry."""

from datetime import UTC, datetime
from time import perf_counter, sleep
from uuid import UUID

import structlog
from celery import Celery  # type: ignore[import-untyped]
from celery.signals import (  # type: ignore[import-untyped]
    before_task_publish,
    task_postrun,
    task_prerun,
)

from vittavaan.config import get_settings
from vittavaan.infrastructure.cache import increment_worker_metrics
from vittavaan.logging import configure_logging
from vittavaan.telemetry import MetricsRegistry

settings = get_settings()
configure_logging()
logger = structlog.get_logger()
task_started_at: dict[str, float] = {}
worker_metrics = MetricsRegistry()
celery_app = Celery("vittavaan", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_soft_time_limit=60,
    task_time_limit=90,
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=12,
    broker_transport_options={
        "socket_connect_timeout": 5,
        "socket_timeout": 5,
        "visibility_timeout": settings.WORKER_VISIBILITY_TIMEOUT_SECONDS,
    },
    result_backend_transport_options={
        "retry_policy": {"timeout": 5.0},
        "visibility_timeout": settings.WORKER_VISIBILITY_TIMEOUT_SECONDS,
    },
    visibility_timeout=settings.WORKER_VISIBILITY_TIMEOUT_SECONDS,
    worker_cancel_long_running_tasks_on_connection_loss=True,
    worker_enable_prefetch_count_reduction=True,
)


@before_task_publish.connect  # type: ignore[untyped-decorator]
def record_enqueue_time(headers: dict[str, object] | None = None, **_kwargs: object) -> None:
    """Add a technical UTC timestamp used only to calculate queue age."""

    if headers is not None:
        headers["vittavaan_enqueued_at"] = datetime.now(UTC).isoformat()


@task_prerun.connect  # type: ignore[untyped-decorator]
def record_task_start(
    task_id: str | None = None, task: object | None = None, **_kwargs: object
) -> None:
    """Record technical task timing without arguments or payloads."""

    structlog.contextvars.clear_contextvars()
    request = getattr(task, "request", None)
    headers = getattr(request, "headers", None) or {}
    if isinstance(headers, dict):
        trace_context: dict[str, str] = {}
        for name in ("correlation_id", "causation_id"):
            raw_value = headers.get(f"vittavaan_{name}")
            try:
                if raw_value:
                    trace_context[name] = str(UUID(str(raw_value)))
            except ValueError:
                continue
        structlog.contextvars.bind_contextvars(**trace_context)
    if task_id:
        task_started_at[task_id] = perf_counter()
    logger.info(
        "worker_task_started",
        service="worker",
        task_name=getattr(task, "name", "unknown"),
    )


@task_postrun.connect  # type: ignore[untyped-decorator]
def record_task_finish(
    task_id: str | None = None,
    task: object | None = None,
    state: str | None = None,
    **_kwargs: object,
) -> None:
    """Record bounded worker outcome and runtime labels."""

    started_at = task_started_at.pop(task_id, None) if task_id else None
    duration_seconds = perf_counter() - started_at if started_at else None
    duration_ms = round(duration_seconds * 1000, 3) if duration_seconds is not None else None
    task_name = str(getattr(task, "name", "unknown"))
    if duration_seconds is not None:
        try:
            increments = worker_metrics.worker_task_finished(
                task_name=task_name,
                state=state or "UNKNOWN",
                duration_seconds=duration_seconds,
            )
            increment_worker_metrics(str(settings.REDIS_URL), increments)
        except ValueError:
            logger.warning("worker_task_metric_rejected", service="worker")
        except Exception:
            logger.warning("worker_task_metric_store_unavailable", service="worker")
    logger.info(
        "worker_task_completed",
        service="worker",
        task_name=task_name,
        state=state or "unknown",
        duration_ms=duration_ms,
    )
    structlog.contextvars.clear_contextvars()


@celery_app.task(name="foundation.smoke.v1")  # type: ignore[untyped-decorator]
def smoke_task(correlation_id: str, causation_id: str | None = None) -> dict[str, str]:
    """Return a deterministic result without creating a business fact."""

    structlog.contextvars.bind_contextvars(
        correlation_id=correlation_id,
        causation_id=causation_id or correlation_id,
    )
    return {"status": "ok", "correlation_id": correlation_id}


@celery_app.task(name="foundation.recovery_probe.v1")  # type: ignore[untyped-decorator]
def recovery_probe_task(correlation_id: str, duration_seconds: int = 20) -> dict[str, str]:
    """Synthetic long-running task used only for worker interruption drills."""

    bounded_duration = min(max(duration_seconds, 1), 45)
    structlog.contextvars.bind_contextvars(
        correlation_id=correlation_id,
        causation_id=correlation_id,
    )
    sleep(bounded_duration)
    return {"status": "recovered", "correlation_id": correlation_id}
