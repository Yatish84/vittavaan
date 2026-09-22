"""FastAPI application factory and foundation health contracts."""

import hmac
import secrets
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from time import perf_counter
from typing import Annotated, cast
from urllib.parse import urlencode
from uuid import UUID, uuid4

import structlog
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.exceptions import HTTPException as StarletteHTTPException

from vittavaan.application.principal_bootstrap import (
    LocalPrincipalDeniedError,
    PrincipalBootstrapControl,
)
from vittavaan.boundary.authentication import require_verified_identity
from vittavaan.config import Settings, get_settings
from vittavaan.domain.identity import VerifiedIdentity
from vittavaan.domain.principal import PrincipalStatus, PrincipalType
from vittavaan.infrastructure.auth_core import (
    AuthCoreHandoffClient,
    AuthCoreVerifier,
    AuthHandoffRejectedError,
    AuthVerifierUnavailableError,
)
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
from vittavaan.infrastructure.principals import PostgresPrincipalRepository
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


class BootstrapPrincipalResponse(BaseModel):
    """Safe application-local identity returned to the frontend."""

    principal_id: UUID
    principal_type: PrincipalType
    status: PrincipalStatus


class BootstrapResponse(BaseModel):
    """Minimum S2 entry state; S3 adds authorized household scopes."""

    principal: BootstrapPrincipalResponse
    first_run_required: bool
    next_route: str
    permitted_person_ids: list[UUID]
    permitted_household_ids: list[UUID]


class HandoffStartResponse(BaseModel):
    authorization_url: str


class HandoffExchangeRequest(BaseModel):
    code: str = Field(min_length=32, max_length=256)
    state: str = Field(min_length=32, max_length=256)


class HandoffExchangeResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


def _handoff_cookie_name(settings: Settings) -> str:
    return (
        "vittavaan_handoff_state"
        if settings.APP_ENV in {"local", "test"}
        else "__Host-vittavaan_handoff_state"
    )


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
        auth_core_verifier = AuthCoreVerifier(
            base_url=str(runtime_settings.AUTH_CORE_VERIFIER_URL),
            timeout_seconds=runtime_settings.AUTH_VERIFIER_TIMEOUT_SECONDS,
            allowed_client_types=runtime_settings.AUTH_ALLOWED_CLIENT_TYPES,
        )
        auth_core_handoff = AuthCoreHandoffClient(
            base_url=str(runtime_settings.AUTH_CORE_API_URL),
            client_secret=cast(str, runtime_settings.AUTH_CORE_HANDOFF_CLIENT_SECRET),
            timeout_seconds=runtime_settings.AUTH_VERIFIER_TIMEOUT_SECONDS,
        )
        principal_bootstrap = PrincipalBootstrapControl(PostgresPrincipalRepository(engine))
        app.state.database_engine = engine
        app.state.cache = cache
        app.state.auth_core_verifier = auth_core_verifier
        app.state.auth_core_handoff = auth_core_handoff
        app.state.principal_bootstrap = principal_bootstrap
        logger.info(
            "service_started",
            service="api",
            environment=runtime_settings.APP_ENV,
            release_id=runtime_settings.APP_RELEASE_ID,
        )
        try:
            yield
        finally:
            await auth_core_handoff.close()
            await auth_core_verifier.close()
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
        response = JSONResponse(
            status_code=error_status,
            content=problem.model_dump(),
            media_type="application/problem+json",
        )
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exception: StarletteHTTPException
    ) -> JSONResponse:
        if exception.status_code == status.HTTP_401_UNAUTHORIZED:
            response = problem_response(
                request,
                error_status=status.HTTP_401_UNAUTHORIZED,
                title="Authentication required",
                detail="Sign in again to continue.",
                error_type="urn:vittavaan:problem:authentication-required",
            )
            response.headers["WWW-Authenticate"] = "Bearer"
            return response
        if exception.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
            return problem_response(
                request,
                error_status=status.HTTP_503_SERVICE_UNAVAILABLE,
                title="Authentication temporarily unavailable",
                detail="Please try again shortly.",
                error_type="urn:vittavaan:problem:authentication-unavailable",
            )
        if exception.status_code == status.HTTP_403_FORBIDDEN:
            return problem_response(
                request,
                error_status=status.HTTP_403_FORBIDDEN,
                title="Application access denied",
                detail="This Vittavaan profile cannot be used.",
                error_type="urn:vittavaan:problem:application-access-denied",
            )
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

    @app.post("/api/v1/auth/handoff/start", response_model=HandoffStartResponse)
    async def start_auth_handoff(response: Response) -> HandoffStartResponse:
        state_value = secrets.token_urlsafe(32)
        query = urlencode(
            {
                "return_url": str(runtime_settings.AUTH_RETURN_URL),
                "state": state_value,
            }
        )
        response.set_cookie(
            _handoff_cookie_name(runtime_settings),
            state_value,
            max_age=300,
            secure=runtime_settings.APP_ENV not in {"local", "test"},
            httponly=True,
            samesite="lax",
            path="/",
        )
        response.headers["Cache-Control"] = "no-store"
        return HandoffStartResponse(
            authorization_url=f"{str(runtime_settings.AUTH_CORE_WEB_URL).rstrip('/')}/login?{query}"
        )

    @app.post("/api/v1/auth/handoff/exchange", response_model=HandoffExchangeResponse)
    async def exchange_auth_handoff(
        payload: HandoffExchangeRequest,
        request: Request,
        response: Response,
    ) -> HandoffExchangeResponse:
        cookie_name = _handoff_cookie_name(runtime_settings)
        expected_state = request.cookies.get(cookie_name)
        if not expected_state or not hmac.compare_digest(expected_state, payload.state):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        handoff = cast(AuthCoreHandoffClient, request.app.state.auth_core_handoff)
        try:
            access_token = await handoff.exchange(
                code=payload.code,
                return_url=str(runtime_settings.AUTH_RETURN_URL),
            )
        except AuthHandoffRejectedError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from exc
        except AuthVerifierUnavailableError as exc:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE) from exc
        response.delete_cookie(
            cookie_name,
            secure=runtime_settings.APP_ENV not in {"local", "test"},
            httponly=True,
            samesite="lax",
            path="/",
        )
        response.headers["Cache-Control"] = "no-store"
        return HandoffExchangeResponse(access_token=access_token)

    @app.get("/api/v1/bootstrap", response_model=BootstrapResponse)
    async def bootstrap(
        request: Request,
        identity: Annotated[VerifiedIdentity, Depends(require_verified_identity)],
    ) -> BootstrapResponse:
        control = cast(PrincipalBootstrapControl, request.app.state.principal_bootstrap)
        try:
            result = await control.bootstrap(identity)
        except LocalPrincipalDeniedError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc
        principal = result.principal
        # Person/household links intentionally begin in S3. Until then every
        # authenticated principal is routed to the first-run experience.
        return BootstrapResponse(
            principal=BootstrapPrincipalResponse(
                principal_id=principal.principal_id,
                principal_type=principal.principal_type,
                status=principal.status,
            ),
            first_run_required=True,
            next_route="/account-setup",
            permitted_person_ids=[],
            permitted_household_ids=[],
        )

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
