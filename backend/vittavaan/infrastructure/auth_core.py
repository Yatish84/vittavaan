"""Fail-closed HTTP adapter for auth-core's revocation-aware verifier."""

from datetime import datetime

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from vittavaan.domain.identity import VerifiedIdentity


class AuthTokenRejectedError(Exception):
    """The supplied access token was rejected by auth-core."""


class AuthVerifierUnavailableError(Exception):
    """auth-core could not provide a trustworthy verification result."""


class AuthHandoffRejectedError(Exception):
    """The one-time auth-core handoff was invalid, expired or already used."""


class _VerifiedClaims(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str = Field(min_length=1, max_length=255)
    session_id: str = Field(min_length=1)
    family_id: str = Field(min_length=1)
    jti: str = Field(min_length=1)
    client_type: str = Field(min_length=1)
    assurance: list[str]
    workspace_id: str | None = None
    workspace_type: str | None = None
    roles: list[str] = Field(default_factory=list)
    issued_at: datetime = Field(alias="IssuedAt")


class _HandoffExchangeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str = Field(min_length=20, max_length=8192)
    token_type: str = Field(pattern="^Bearer$")


class AuthCoreVerifier:
    """Verify bearer tokens without decoding or persisting them in Vittavaan."""

    def __init__(
        self,
        *,
        base_url: str,
        timeout_seconds: float,
        allowed_client_types: frozenset[str],
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._allowed_client_types = allowed_client_types
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=httpx.Timeout(timeout_seconds),
            follow_redirects=False,
        )

    async def close(self) -> None:
        """Close the internally owned connection pool."""

        if self._owns_client:
            await self._client.aclose()

    async def verify(self, bearer_token: str) -> VerifiedIdentity:
        """Return trusted identity facts or a bounded fail-closed error."""

        if not bearer_token or any(character.isspace() for character in bearer_token):
            raise AuthTokenRejectedError
        try:
            response = await self._client.get(
                "/verify",
                headers={"Authorization": f"Bearer {bearer_token}"},
            )
        except httpx.RequestError as exc:
            raise AuthVerifierUnavailableError from exc

        if response.status_code == 401:
            raise AuthTokenRejectedError
        if response.status_code != 200:
            raise AuthVerifierUnavailableError

        try:
            claims = _VerifiedClaims.model_validate(response.json())
        except (ValueError, ValidationError) as exc:
            raise AuthVerifierUnavailableError from exc
        if claims.client_type not in self._allowed_client_types:
            raise AuthTokenRejectedError

        return VerifiedIdentity(
            auth_subject=claims.user_id,
            session_id=claims.session_id,
            token_family_id=claims.family_id,
            token_id=claims.jti,
            client_type=claims.client_type,
            assurance=tuple(claims.assurance),
            issued_at=claims.issued_at,
            workspace_id=claims.workspace_id,
            workspace_type=claims.workspace_type,
            roles=tuple(claims.roles),
        )


class AuthCoreHandoffClient:
    """Server-to-server exchange of a single-use code for an access token."""

    def __init__(
        self,
        *,
        base_url: str,
        client_secret: str,
        timeout_seconds: float,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._client_secret = client_secret
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=httpx.Timeout(timeout_seconds),
            follow_redirects=False,
        )

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def exchange(self, *, code: str, return_url: str) -> str:
        try:
            response = await self._client.post(
                "/api/v1/auth/handoff/exchange",
                headers={"X-Handoff-Client-Secret": self._client_secret},
                json={"code": code, "return_url": return_url},
            )
        except httpx.RequestError as exc:
            raise AuthVerifierUnavailableError from exc
        if response.status_code in {400, 401}:
            raise AuthHandoffRejectedError
        if response.status_code != 200:
            raise AuthVerifierUnavailableError
        try:
            payload = _HandoffExchangeResponse.model_validate(response.json())
        except (ValueError, ValidationError) as exc:
            raise AuthVerifierUnavailableError from exc
        return payload.access_token
