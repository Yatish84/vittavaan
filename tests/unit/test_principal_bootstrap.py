"""Application rules for local principal bootstrap."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from vittavaan.application.principal_bootstrap import (
    LocalPrincipalDeniedError,
    PrincipalBootstrapControl,
)
from vittavaan.domain.identity import VerifiedIdentity
from vittavaan.domain.principal import (
    AppPrincipal,
    PrincipalBootstrapResult,
    PrincipalStatus,
    PrincipalType,
)

NOW = datetime(2026, 9, 21, 12, tzinfo=UTC)


class FakeRepository:
    def __init__(self, principal: AppPrincipal) -> None:
        self.principal = principal
        self.received: tuple[str, datetime] | None = None

    async def bootstrap(
        self, *, auth_subject_id: str, seen_at: datetime
    ) -> PrincipalBootstrapResult:
        self.received = (auth_subject_id, seen_at)
        return PrincipalBootstrapResult(self.principal, created=False)


def principal(status: PrincipalStatus = PrincipalStatus.ACTIVE) -> AppPrincipal:
    return AppPrincipal(
        principal_id=uuid4(),
        auth_subject_id="auth-user-1",
        principal_type=PrincipalType.PERSON,
        status=status,
        first_seen_at=NOW,
        last_seen_at=NOW,
        created_at=NOW,
        updated_at=NOW,
        version=1,
    )


def identity() -> VerifiedIdentity:
    return VerifiedIdentity(
        auth_subject="auth-user-1",
        session_id="session-1",
        token_family_id="family-1",
        token_id="token-1",
        client_type="web",
        assurance=("pwd",),
        issued_at=NOW,
    )


@pytest.mark.asyncio
async def test_bootstrap_uses_verified_subject_and_controlled_clock() -> None:
    repository = FakeRepository(principal())
    control = PrincipalBootstrapControl(repository, clock=lambda: NOW)

    result = await control.bootstrap(identity())

    assert result.principal.auth_subject_id == "auth-user-1"
    assert repository.received == ("auth-user-1", NOW)


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [PrincipalStatus.SUSPENDED, PrincipalStatus.CLOSED])
async def test_bootstrap_denies_inactive_local_principal(status: PrincipalStatus) -> None:
    control = PrincipalBootstrapControl(FakeRepository(principal(status)), clock=lambda: NOW)

    with pytest.raises(LocalPrincipalDeniedError):
        await control.bootstrap(identity())
