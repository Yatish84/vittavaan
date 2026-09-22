"""API contract for the authenticated application bootstrap endpoint."""

from datetime import UTC, datetime
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient
from vittavaan.application.principal_bootstrap import LocalPrincipalDeniedError
from vittavaan.boundary.api import create_app
from vittavaan.config import Settings
from vittavaan.domain.identity import VerifiedIdentity
from vittavaan.domain.principal import (
    AppPrincipal,
    PrincipalBootstrapResult,
    PrincipalStatus,
    PrincipalType,
)

NOW = datetime(2026, 9, 22, 12, tzinfo=UTC)
PRINCIPAL_ID = UUID("0199a000-0000-7000-8000-000000000001")


class FakeVerifier:
    async def verify(self, _token: str) -> VerifiedIdentity:
        return VerifiedIdentity(
            auth_subject="auth-user-1",
            session_id="session-1",
            token_family_id="family-1",
            token_id="token-1",
            client_type="web",
            assurance=("pwd",),
            issued_at=NOW,
        )


class FakeBootstrapControl:
    def __init__(self, status: PrincipalStatus) -> None:
        self.status = status

    async def bootstrap(self, _identity: VerifiedIdentity) -> PrincipalBootstrapResult:
        principal = AppPrincipal(
            principal_id=PRINCIPAL_ID,
            auth_subject_id="auth-user-1",
            principal_type=PrincipalType.PERSON,
            status=self.status,
            first_seen_at=NOW,
            last_seen_at=NOW,
            created_at=NOW,
            updated_at=NOW,
            version=1,
        )
        if self.status is not PrincipalStatus.ACTIVE:
            raise LocalPrincipalDeniedError
        return PrincipalBootstrapResult(principal, created=True)


def build_app(status: PrincipalStatus = PrincipalStatus.ACTIVE):
    settings = Settings(
        APP_ENV="test",
        APP_RELEASE_ID="test-release",
        DATABASE_URL="postgresql+asyncpg://user:secret@localhost/test",
        REDIS_URL="redis://:secret@localhost:6379/0",
    )
    app = create_app(settings)
    app.state.auth_core_verifier = FakeVerifier()
    app.state.principal_bootstrap = FakeBootstrapControl(status)
    return app


@pytest.mark.asyncio
async def test_new_principal_receives_first_run_bootstrap() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=build_app()), base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/v1/bootstrap", headers={"Authorization": "Bearer signed-token"}
        )

    assert response.status_code == 200
    assert response.json() == {
        "principal": {
            "principal_id": str(PRINCIPAL_ID),
            "principal_type": "PERSON",
            "status": "ACTIVE",
        },
        "first_run_required": True,
        "next_route": "/account-setup",
        "permitted_person_ids": [],
        "permitted_household_ids": [],
    }


@pytest.mark.asyncio
async def test_suspended_principal_is_denied_even_with_valid_auth_identity() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=build_app(PrincipalStatus.SUSPENDED)),
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/api/v1/bootstrap", headers={"Authorization": "Bearer signed-token"}
        )

    assert response.status_code == 403
    assert response.json()["type"] == "urn:vittavaan:problem:application-access-denied"
