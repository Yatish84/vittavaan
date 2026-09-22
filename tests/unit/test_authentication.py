"""Protected-route behavior at the Vittavaan API boundary."""

from datetime import UTC, datetime
from typing import Annotated

import pytest
from fastapi import Depends
from httpx import ASGITransport, AsyncClient
from vittavaan.boundary.api import create_app
from vittavaan.boundary.authentication import require_verified_identity
from vittavaan.config import Settings
from vittavaan.domain.identity import VerifiedIdentity
from vittavaan.infrastructure.auth_core import (
    AuthTokenRejectedError,
    AuthVerifierUnavailableError,
)


class FakeVerifier:
    def __init__(self, result: VerifiedIdentity | Exception) -> None:
        self.result = result

    async def verify(self, _token: str) -> VerifiedIdentity:
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def build_test_app(result: VerifiedIdentity | Exception):
    settings = Settings(
        APP_ENV="test",
        APP_RELEASE_ID="test-release",
        DATABASE_URL="postgresql+asyncpg://user:secret@localhost/test",
        REDIS_URL="redis://:secret@localhost:6379/0",
    )
    app = create_app(settings)
    app.state.auth_core_verifier = FakeVerifier(result)

    @app.get("/test/protected")
    async def protected(
        identity: Annotated[VerifiedIdentity, Depends(require_verified_identity)],
    ) -> dict[str, str]:
        return {"auth_subject": identity.auth_subject}

    return app


def identity() -> VerifiedIdentity:
    return VerifiedIdentity(
        auth_subject="user-1",
        session_id="session-1",
        token_family_id="family-1",
        token_id="token-1",
        client_type="web",
        assurance=("pwd",),
        issued_at=datetime(2026, 9, 21, tzinfo=UTC),
    )


@pytest.mark.asyncio
async def test_protected_dependency_returns_verified_identity() -> None:
    transport = ASGITransport(app=build_test_app(identity()))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/test/protected", headers={"Authorization": "Bearer signed-token"}
        )

    assert response.status_code == 200
    assert response.json() == {"auth_subject": "user-1"}


@pytest.mark.asyncio
@pytest.mark.parametrize("headers", [{}, {"Authorization": "Basic credentials"}])
async def test_missing_or_wrong_authentication_is_safe(headers: dict[str, str]) -> None:
    transport = ASGITransport(app=build_test_app(identity()))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/test/protected", headers=headers)

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json()["type"] == "urn:vittavaan:problem:authentication-required"


@pytest.mark.asyncio
async def test_rejected_token_is_unauthenticated() -> None:
    transport = ASGITransport(app=build_test_app(AuthTokenRejectedError()))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/test/protected", headers={"Authorization": "Bearer rejected-token"}
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_verifier_outage_is_distinct_and_fails_closed() -> None:
    transport = ASGITransport(app=build_test_app(AuthVerifierUnavailableError()))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/test/protected", headers={"Authorization": "Bearer signed-token"}
        )

    assert response.status_code == 503
    assert response.json()["type"] == "urn:vittavaan:problem:authentication-unavailable"
