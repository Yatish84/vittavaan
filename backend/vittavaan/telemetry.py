"""Low-cardinality metrics and OpenTelemetry-compatible tracing foundations."""

from collections import Counter
from dataclasses import dataclass, field
from threading import Lock

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

HTTP_DURATION_BUCKETS = (0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
WORKER_DURATION_BUCKETS = (0.1, 0.5, 1.0, 5.0, 15.0, 30.0, 60.0, 90.0)
APPROVED_WORKER_TASKS = {"foundation.smoke.v1", "foundation.recovery_probe.v1"}
APPROVED_WORKER_STATES = {"SUCCESS", "FAILURE", "RETRY", "REVOKED", "UNKNOWN"}
WORKER_TASK_ALIASES = {
    "foundation.smoke.v1": "smoke",
    "foundation.recovery_probe.v1": "recovery_probe",
}
WORKER_TASKS_BY_ALIAS = {alias: name for name, alias in WORKER_TASK_ALIASES.items()}
tracer = trace.get_tracer("vittavaan.api")
_trace_exporter: InMemorySpanExporter | None = None


def configure_local_tracing(
    *, service: str, environment: str, release_id: str
) -> InMemorySpanExporter:
    """Install a process-local safe exporter without network or credential output."""

    global _trace_exporter
    if _trace_exporter is None:
        provider = TracerProvider(
            resource=Resource.create(
                {
                    "service.name": service,
                    "deployment.environment.name": environment,
                    "service.version": release_id,
                }
            )
        )
        _trace_exporter = InMemorySpanExporter()
        provider.add_span_processor(SimpleSpanProcessor(_trace_exporter))
        trace.set_tracer_provider(provider)
    return _trace_exporter


@dataclass
class MetricsRegistry:
    """Small process-local Prometheus registry with strictly bounded labels."""

    request_totals: Counter[tuple[str, str, str]] = field(default_factory=Counter)
    duration_buckets: Counter[tuple[str, str, float]] = field(default_factory=Counter)
    dependency_ready: dict[str, bool] = field(default_factory=dict)
    database_pool: dict[str, int] = field(default_factory=dict)
    queue_depth: int = 0
    queue_oldest_age_seconds: float = 0.0
    worker_task_totals: Counter[tuple[str, str]] = field(default_factory=Counter)
    worker_duration_buckets: Counter[tuple[str, float]] = field(default_factory=Counter)
    inflight: int = 0
    _lock: Lock = field(default_factory=Lock)

    def request_started(self) -> None:
        with self._lock:
            self.inflight += 1

    def request_finished(
        self, *, method: str, route: str, status_code: int, duration_seconds: float
    ) -> None:
        status_class = f"{status_code // 100}xx"
        with self._lock:
            self.inflight -= 1
            self.request_totals[(method, route, status_class)] += 1
            for bucket in HTTP_DURATION_BUCKETS:
                if duration_seconds <= bucket:
                    self.duration_buckets[(method, route, bucket)] += 1

    def set_dependency_ready(self, dependency: str, ready: bool) -> None:
        """Set a bounded dependency health gauge."""

        if dependency not in {"postgres", "valkey"}:
            raise ValueError("Unsupported dependency metric label")
        with self._lock:
            self.dependency_ready[dependency] = ready

    def set_database_pool(self, *, size: int, checked_out: int, overflow: int) -> None:
        """Record bounded SQLAlchemy pool capacity without connection details."""

        values = {"size": size, "checked_out": checked_out, "overflow": overflow}
        if any(value < 0 for value in values.values()):
            raise ValueError("Database pool metrics cannot be negative")
        with self._lock:
            self.database_pool = values

    def set_queue_status(self, *, depth: int, oldest_age_seconds: float) -> None:
        """Record aggregate broker pressure without inspecting task arguments."""

        if depth < 0 or oldest_age_seconds < 0:
            raise ValueError("Queue metrics cannot be negative")
        with self._lock:
            self.queue_depth = depth
            self.queue_oldest_age_seconds = oldest_age_seconds

    def worker_task_finished(
        self, *, task_name: str, state: str, duration_seconds: float
    ) -> dict[str, int]:
        """Record only explicitly approved task and outcome labels."""

        if task_name not in APPROVED_WORKER_TASKS:
            raise ValueError("Unsupported worker task metric label")
        normalized_state = state.upper()
        if normalized_state not in APPROVED_WORKER_STATES:
            normalized_state = "UNKNOWN"
        if duration_seconds < 0:
            raise ValueError("Worker duration cannot be negative")
        alias = WORKER_TASK_ALIASES[task_name]
        increments = {f"total|{alias}|{normalized_state}": 1}
        with self._lock:
            self.worker_task_totals[(task_name, normalized_state)] += 1
            for bucket in WORKER_DURATION_BUCKETS:
                if duration_seconds <= bucket:
                    self.worker_duration_buckets[(task_name, bucket)] += 1
                    increments[f"bucket|{alias}|{bucket}"] = 1
        return increments

    def replace_worker_snapshot(self, snapshot: dict[str, int]) -> None:
        """Load aggregate worker counters from the shared technical store."""

        totals: Counter[tuple[str, str]] = Counter()
        buckets: Counter[tuple[str, float]] = Counter()
        for metric_field, value in snapshot.items():
            if value < 0:
                raise ValueError("Worker metric values cannot be negative")
            parts = metric_field.split("|")
            if len(parts) != 3 or parts[1] not in WORKER_TASKS_BY_ALIAS:
                raise ValueError("Unsupported stored worker metric")
            metric_type, alias, final_value = parts
            task_name = WORKER_TASKS_BY_ALIAS[alias]
            if metric_type == "total" and final_value in APPROVED_WORKER_STATES:
                totals[(task_name, final_value)] = value
            elif metric_type == "bucket" and float(final_value) in WORKER_DURATION_BUCKETS:
                buckets[(task_name, float(final_value))] = value
            else:
                raise ValueError("Unsupported stored worker metric")
        with self._lock:
            self.worker_task_totals = totals
            self.worker_duration_buckets = buckets

    def render_prometheus(self) -> str:
        """Render safe Prometheus text without IDs, URLs or financial values."""

        lines = [
            "# HELP vittavaan_http_requests_inflight Current in-flight HTTP requests.",
            "# TYPE vittavaan_http_requests_inflight gauge",
            f"vittavaan_http_requests_inflight {self.inflight}",
            "# HELP vittavaan_dependency_ready Required dependency readiness.",
            "# TYPE vittavaan_dependency_ready gauge",
            "# HELP vittavaan_database_pool_connections Database pool capacity and use.",
            "# TYPE vittavaan_database_pool_connections gauge",
            "# HELP vittavaan_worker_queue_depth Tasks waiting in the bounded worker queue.",
            "# TYPE vittavaan_worker_queue_depth gauge",
            f"vittavaan_worker_queue_depth {self.queue_depth}",
            "# HELP vittavaan_worker_queue_oldest_age_seconds Age of the oldest queued task.",
            "# TYPE vittavaan_worker_queue_oldest_age_seconds gauge",
            f"vittavaan_worker_queue_oldest_age_seconds {self.queue_oldest_age_seconds}",
            "# HELP vittavaan_http_requests_total Completed HTTP requests.",
            "# TYPE vittavaan_http_requests_total counter",
        ]
        with self._lock:
            for dependency, ready in sorted(self.dependency_ready.items()):
                lines.append(
                    f'vittavaan_dependency_ready{{dependency="{dependency}"}} {int(ready)}'
                )
            for state, value in sorted(self.database_pool.items()):
                lines.append(f'vittavaan_database_pool_connections{{state="{state}"}} {value}')
            for (method, route, status_class), value in sorted(self.request_totals.items()):
                labels = f'method="{method}",route="{route}",status_class="{status_class}"'
                lines.append(f"vittavaan_http_requests_total{{{labels}}} {value}")
            lines.extend(
                [
                    "# HELP vittavaan_http_request_duration_seconds HTTP request latency buckets.",
                    "# TYPE vittavaan_http_request_duration_seconds histogram",
                ]
            )
            for (method, route, bucket), value in sorted(self.duration_buckets.items()):
                labels = f'method="{method}",route="{route}",le="{bucket}"'
                lines.append(f"vittavaan_http_request_duration_seconds_bucket{{{labels}}} {value}")
            lines.extend(
                [
                    "# HELP vittavaan_worker_tasks_total Completed worker tasks.",
                    "# TYPE vittavaan_worker_tasks_total counter",
                ]
            )
            for (task_name, state), value in sorted(self.worker_task_totals.items()):
                labels = f'task_name="{task_name}",state="{state}"'
                lines.append(f"vittavaan_worker_tasks_total{{{labels}}} {value}")
            lines.extend(
                [
                    "# HELP vittavaan_worker_task_duration_seconds Worker runtime buckets.",
                    "# TYPE vittavaan_worker_task_duration_seconds histogram",
                ]
            )
            for (task_name, bucket), value in sorted(self.worker_duration_buckets.items()):
                labels = f'task_name="{task_name}",le="{bucket}"'
                lines.append(f"vittavaan_worker_task_duration_seconds_bucket{{{labels}}} {value}")
        return "\n".join(lines) + "\n"
