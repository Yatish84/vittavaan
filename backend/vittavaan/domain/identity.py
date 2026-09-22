"""Authentication identity understood by the Vittavaan domain."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class VerifiedIdentity:
    """Immutable identity facts verified by auth-core, without wealth permissions."""

    auth_subject: str
    session_id: str
    token_family_id: str
    token_id: str
    client_type: str
    assurance: tuple[str, ...]
    issued_at: datetime
    workspace_id: str | None = None
    workspace_type: str | None = None
    roles: tuple[str, ...] = ()
