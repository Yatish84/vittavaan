"""Monitoring safety, cardinality and redaction tests."""

import pytest
from httpx import ASGITransport, AsyncClient
from vittavaan.boundary.api import create_app
from vittavaan.config import Settings
from vittavaan.logging import redact_sensitive_fields
from vittavaan.telemetry import MetricsRegistry, configure_local_tracing

CANARY = "VITTAVAAN_FAKE_SECRET_CANARY_7f4d8b"


def settings_with_canary() -> Settings:
    return Settings(
        APP_ENV="test",
        APP_RELEASE_ID="telemetry-test",
        DATABASE_URL=f"postgresql+asyncpg://user:{CANARY}@localhost/test",
        REDIS_URL=f"redis://:{CANARY}@localhost:6379/0",
    )


def test_sensitive_fields_are_recursively_redacted() -> None:
    event = {
        "event": "canary_test",
        "password": CANARY,
        "nested": {"authorization_header": CANARY, "safe": "visible"},
        "items": [{"access_token": CANARY}],
    }
    redacted = redact_sensitive_fields(None, "info", event)

    assert CANARY not in repr(redacted)
    assert redacted["password"] == "[REDACTED]"
    assert redacted["nested"] == {"authorization_header": "[REDACTED]", "safe": "visible"}


def test_metrics_use_only_bounded_technical_labels() -> None:
    registry = MetricsRegistry()
    registry.request_started()
    registry.request_finished(
        method="GET", route="/health/live", status_code=200, duration_seconds=0.02
    )
    registry.set_dependency_ready("postgres", True)
    registry.set_database_pool(size=5, checked_out=2, overflow=0)
    registry.set_queue_status(depth=3, oldest_age_seconds=1.25)
    registry.worker_task_finished(
        task_name="foundation.smoke.v1", state="SUCCESS", duration_seconds=0.2
    )
    output = registry.render_prometheus()

    assert 'method="GET",route="/health/live",status_class="2xx"' in output
    assert "correlation" not in output
    assert "user" not in output
    assert CANARY not in output
    assert 'vittavaan_dependency_ready{dependency="postgres"} 1' in output
    assert 'vittavaan_database_pool_connections{state="checked_out"} 2' in output
    assert "vittavaan_worker_queue_depth 3" in output
    assert "vittavaan_worker_queue_oldest_age_seconds 1.25" in output
    assert 'task_name="foundation.smoke.v1",state="SUCCESS"' in output


def test_metrics_reject_unbounded_dependency_labels() -> None:
    registry = MetricsRegistry()
    try:
        registry.set_dependency_ready("customer-supplied-value", True)
    except ValueError as exc:
        assert str(exc) == "Unsupported dependency metric label"
    else:
        raise AssertionError("Unbounded dependency label was accepted")

    with pytest.raises(ValueError, match="Unsupported worker task metric label"):
        registry.worker_task_finished(
            task_name="customer-controlled-task", state="SUCCESS", duration_seconds=1
        )
    with pytest.raises(ValueError, match="cannot be negative"):
        registry.set_queue_status(depth=-1, oldest_age_seconds=0)
    with pytest.raises(ValueError, match="Unsupported stored worker metric"):
        registry.replace_worker_snapshot({"total|customer-value|SUCCESS": 1})


def test_worker_snapshot_replaces_process_local_values() -> None:
    registry = MetricsRegistry()
    registry.worker_task_finished(
        task_name="foundation.smoke.v1", state="SUCCESS", duration_seconds=0.2
    )
    registry.replace_worker_snapshot(
        {
            "total|recovery_probe|SUCCESS": 2,
            "bucket|recovery_probe|30.0": 2,
        }
    )
    output = registry.render_prometheus()

    assert 'task_name="foundation.recovery_probe.v1",state="SUCCESS"} 2' in output
    assert 'task_name="foundation.smoke.v1"' not in output


async def test_health_metrics_openapi_and_settings_do_not_expose_canary() -> None:
    settings = settings_with_canary()
    exporter = configure_local_tracing(
        service="api", environment="test", release_id="telemetry-test"
    )
    exporter.clear()
    app = create_app(settings)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        health = await client.get("/health/live")
        metrics = await client.get("/metrics")

    combined = health.text + metrics.text + repr(settings) + str(app.openapi())
    assert CANARY not in combined
    assert "/metrics" not in app.openapi()["paths"]
    assert "vittavaan_http_requests_total" in metrics.text
    assert 'route="/health/live"' in metrics.text
    spans = exporter.get_finished_spans()
    assert spans
    assert CANARY not in repr(spans)
    assert any(span.attributes.get("http.route") == "/health/live" for span in spans)
