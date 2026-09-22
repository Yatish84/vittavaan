"""Application-local principal model; authentication remains in auth-core."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class PrincipalType(StrEnum):
    PERSON = "PERSON"
    SERVICE = "SERVICE"
    SUPPORT = "SUPPORT"


class PrincipalStatus(StrEnum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"


@dataclass(frozen=True, slots=True)
class AppPrincipal:
    """Minimal local authorization identity mapped from an auth-core subject."""

    principal_id: UUID
    auth_subject_id: str
    principal_type: PrincipalType
    status: PrincipalStatus
    first_seen_at: datetime
    last_seen_at: datetime
    created_at: datetime
    updated_at: datetime
    version: int


@dataclass(frozen=True, slots=True)
class PrincipalBootstrapResult:
    principal: AppPrincipal
    created: bool
