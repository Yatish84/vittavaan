"""PostgreSQL persistence for the minimal local principal projection."""

from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from vittavaan.domain.principal import (
    AppPrincipal,
    PrincipalBootstrapResult,
    PrincipalStatus,
    PrincipalType,
)

_INSERT = text(
    """
    INSERT INTO app_principals (auth_subject_id, first_seen_at, last_seen_at)
    VALUES (:auth_subject_id, :seen_at, :seen_at)
    ON CONFLICT (auth_subject_id) DO NOTHING
    RETURNING *
    """
)

_UPDATE_LAST_SEEN = text(
    """
    UPDATE app_principals
    SET last_seen_at = GREATEST(last_seen_at, :seen_at),
        updated_at = CASE WHEN :seen_at > last_seen_at THEN now() ELSE updated_at END,
        version = CASE WHEN :seen_at > last_seen_at THEN version + 1 ELSE version END
    WHERE auth_subject_id = :auth_subject_id
    RETURNING *
    """
)


def _to_principal(row: dict[str, Any]) -> AppPrincipal:
    return AppPrincipal(
        principal_id=row["principal_id"],
        auth_subject_id=row["auth_subject_id"],
        principal_type=PrincipalType(row["principal_type"]),
        status=PrincipalStatus(row["status"]),
        first_seen_at=row["first_seen_at"],
        last_seen_at=row["last_seen_at"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        version=row["version"],
    )


class PostgresPrincipalRepository:
    """Create once by auth subject and safely reuse the same row on retries."""

    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

    async def bootstrap(
        self, *, auth_subject_id: str, seen_at: datetime
    ) -> PrincipalBootstrapResult:
        async with self._engine.begin() as connection:
            inserted = (await connection.execute(
                _INSERT,
                {"auth_subject_id": auth_subject_id, "seen_at": seen_at},
            )).mappings().one_or_none()
            if inserted is not None:
                return PrincipalBootstrapResult(_to_principal(dict(inserted)), created=True)

            existing = (await connection.execute(
                _UPDATE_LAST_SEEN,
                {"auth_subject_id": auth_subject_id, "seen_at": seen_at},
            )).mappings().one()
            return PrincipalBootstrapResult(_to_principal(dict(existing)), created=False)
