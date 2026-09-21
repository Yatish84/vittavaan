"""FastAPI application factory and foundation health contracts."""

from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from time import perf_counter
from uuid import UUID, uuid4

import structlog
from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.exceptions import HTTPException as StarletteHTTPException

from vittavaan.config import Settings, get_settings
from vittavaan.infrastructure.cache import (
    cache_ready,
    create_cache,
    worker_metric_snapshot,
    worker_queue_status,
)
from vittavaan.infrastructure.database import (
    create_engine,
    database_pool_status,
    database_ready,
)
from vittavaan.logging import configure_logging
from vittavaan.telemetry import MetricsRegistry, configure_local_tracing, tracer

logger = structlog.get_logger()


class HealthResponse(BaseModel):
    """Safe public health response."""

    status: str
    release_id: str


class ProblemDetails(BaseModel):
    """RFC 9457-compatible safe error response."""

    type: str
    title: str
    status: int
    detail: str
    instance: str


def _correlation_id(raw_value: str | None) -> str:
    if raw_value:
        try:
            return str(UUID(raw_value))
        except ValueError:
            pass
    return str(uuid4())


def create_app(settings: Settings | None = None) -> FastAPI:
    """Construct the HTTP application without global import-time side effects."""

    configure_logging()
    runtime_settings = settings or get_settings()
    configure_local_tracing(
        service="api",
        environment=runtime_settings.APP_ENV,
        release_id=runtime_settings.APP_RELEASE_ID,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_engine(str(runtime_settings.DATABASE_URL))
        cache = create_cache(str(runtime_settings.REDIS_URL))
        app.state.database_engine = engine
        app.state.cache = cache
        logger.info(
            "service_started",
            service="api",
            environment=runtime_settings.APP_ENV,
            release_id=runtime_settings.APP_RELEASE_ID,
        )
        try:
            yield
        finally:
            await cache.aclose()
            await engine.dispose()
            logger.info("service_stopped", service="api")

    app = FastAPI(title="Vittavaan API", version="0.1.0", lifespan=lifespan)
    app.state.metrics = MetricsRegistry()

    def problem_response(
        request: Request, *, error_status: int, title: str, detail: str, error_type: str
    ) -> JSONResponse:
        problem = ProblemDetails(
            type=error_type,
            title=title,
            status=error_status,
            detail=detail,
            instance=request.url.path,
        )
        return JSONResponse(
            status_code=error_status,
            content=problem.model_dump(),
            media_type="application/problem+json",
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exception: StarletteHTTPException
    ) -> JSONResponse:
        if exception.status_code == status.HTTP_404_NOT_FOUND:
            return problem_response(
                request,
                error_status=status.HTTP_404_NOT_FOUND,
                title="Resource not found",
                detail="The requested resource does not exist.",
                error_type="urn:vittavaan:problem:not-found",
            )
        return problem_response(
            request,
            error_status=exception.status_code,
            title="Request failed",
            detail="The request could not be completed.",
            error_type="urn:vittavaan:problem:http-error",
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, _exception: RequestValidationError
    ) -> JSONResponse:
        return problem_response(
            request,
            error_status=status.HTTP_422_UNPROCESSABLE_CONTENT,
            title="Request validation failed",
            detail="One or more request fields are invalid.",
            error_type="urn:vittavaan:problem:validation",
        )

    @app.middleware("http")
    async def correlation_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        correlation_id = _correlation_id(request.headers.get("X-Correlation-ID"))
        causation_id = _correlation_id(request.headers.get("X-Causation-ID"))
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
        metrics: MetricsRegistry = request.app.state.metrics
        record_metrics = request.url.path != "/metrics"
        started_at = perf_counter()
        if record_metrics:
            metrics.request_started()
        try:
            with tracer.start_as_current_span("http.request") as span:
                span.set_attribute("http.request.method", request.method)
                response = await call_next(request)
                route = getattr(request.scope.get("route"), "path", "unmatched")
                span.set_attribute("http.route", route)
                span.set_attribute("http.response.status_code", response.status_code)
            response.headers["X-Correlation-ID"] = correlation_id
            response.headers["X-Causation-ID"] = causation_id
            if record_metrics:
                duration = perf_counter() - started_at
                metrics.request_finished(
                    method=request.method,
                    route=route,
                    status_code=response.status_code,
                    duration_seconds=duration,
                )
                logger.info(
                    "http_request_completed",
                    service="api",
                    environment=runtime_settings.APP_ENV,
                    release_id=runtime_settings.APP_RELEASE_ID,
                    method=request.method,
                    route=route,
                    status_code=response.status_code,
                    duration_ms=round(duration * 1000, 3),
                    causation_id=causation_id,
                )
            return response
        finally:
            structlog.contextvars.clear_contextvars()

    @app.get("/health/live", response_model=HealthResponse)
    async def live() -> HealthResponse:
        return HealthResponse(status="live", release_id=runtime_settings.APP_RELEASE_ID)

    @app.get("/health/ready", response_model=HealthResponse)
    async def ready(request: Request, response: Response) -> HealthResponse:
        engine: AsyncEngine = request.app.state.database_engine
        cache: Redis = request.app.state.cache
        is_database_ready = await database_ready(engine)
        is_cache_ready = await cache_ready(cache)
        request.app.state.metrics.set_dependency_ready("postgres", is_database_ready)
        request.app.state.metrics.set_dependency_ready("valkey", is_cache_ready)
        request.app.state.metrics.set_database_pool(**database_pool_status(engine))
        if not is_database_ready or not is_cache_ready:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return HealthResponse(status="not_ready", release_id=runtime_settings.APP_RELEASE_ID)
        return HealthResponse(status="ready", release_id=runtime_settings.APP_RELEASE_ID)

    @app.get("/metrics", include_in_schema=False, response_class=PlainTextResponse)
    async def metrics(request: Request) -> PlainTextResponse:
        registry: MetricsRegistry = request.app.state.metrics
        cache: Redis | None = getattr(request.app.state, "cache", None)
        if cache is not None:
            try:
                depth, oldest_age_seconds = await worker_queue_status(cache)
                registry.set_queue_status(
                    depth=depth, oldest_age_seconds=round(oldest_age_seconds, 3)
                )
                registry.replace_worker_snapshot(await worker_metric_snapshot(cache))
            except Exception:
                logger.warning("worker_runtime_metrics_unavailable", service="api")
        return PlainTextResponse(
            registry.render_prometheus(),
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

    return app
