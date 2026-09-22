"""Use case for idempotently establishing a local application principal."""

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Protocol

from vittavaan.domain.identity import VerifiedIdentity
from vittavaan.domain.principal import PrincipalBootstrapResult, PrincipalStatus


class PrincipalRepository(Protocol):
    async def bootstrap(
        self, *, auth_subject_id: str, seen_at: datetime
    ) -> PrincipalBootstrapResult: ...


class LocalPrincipalDeniedError(Exception):
    """The local application principal is not allowed to enter Vittavaan."""


class PrincipalBootstrapControl:
    """Map a verified auth-core identity to one active Vittavaan principal."""

    def __init__(
        self,
        repository: PrincipalRepository,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._repository = repository
        self._clock = clock or (lambda: datetime.now(UTC))

    async def bootstrap(self, identity: VerifiedIdentity) -> PrincipalBootstrapResult:
        result = await self._repository.bootstrap(
            auth_subject_id=identity.auth_subject,
            seen_at=self._clock(),
        )
        if result.principal.status is not PrincipalStatus.ACTIVE:
            raise LocalPrincipalDeniedError
        return result
