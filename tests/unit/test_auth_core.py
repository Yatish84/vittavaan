"""Contract tests for the auth-core verifier adapter."""

import httpx
import pytest
from vittavaan.infrastructure.auth_core import (
    AuthCoreHandoffClient,
    AuthCoreVerifier,
    AuthHandoffRejectedError,
    AuthTokenRejectedError,
    AuthVerifierUnavailableError,
)


def verifier(handler: httpx.MockTransport) -> AuthCoreVerifier:
    client = httpx.AsyncClient(transport=handler, base_url="http://auth-core:8081")
    return AuthCoreVerifier(
        base_url="http://unused",
        timeout_seconds=2,
        allowed_client_types=frozenset({"WEB"}),
        client=client,
    )


@pytest.mark.asyncio
async def test_returns_typed_identity_for_valid_auth_core_response() -> None:
    async def handle(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/verify"
        assert request.headers["Authorization"] == "Bearer signed-token"
        return httpx.Response(
            200,
            json={
                "user_id": "user-1",
                "session_id": "session-1",
                "family_id": "family-1",
                "jti": "token-1",
                "client_type": "WEB",
                "assurance": ["pwd", "mfa"],
                "workspace_id": "workspace-1",
                "workspace_type": "household",
                "roles": ["member"],
                "IssuedAt": "2026-09-21T12:00:00Z",
            },
        )

    adapter = verifier(httpx.MockTransport(handle))
    identity = await adapter.verify("signed-token")

    assert identity.auth_subject == "user-1"
    assert identity.assurance == ("pwd", "mfa")
    assert identity.roles == ("member",)


@pytest.mark.asyncio
async def test_maps_auth_core_rejection_without_exposing_response() -> None:
    adapter = verifier(httpx.MockTransport(lambda _request: httpx.Response(401)))

    with pytest.raises(AuthTokenRejectedError):
        await adapter.verify("rejected-token")


@pytest.mark.asyncio
async def test_rejects_unapproved_client_type() -> None:
    payload = {
        "user_id": "user-1",
        "session_id": "session-1",
        "family_id": "family-1",
        "jti": "token-1",
        "client_type": "service",
        "assurance": [],
        "IssuedAt": "2026-09-21T12:00:00Z",
    }
    adapter = verifier(httpx.MockTransport(lambda _request: httpx.Response(200, json=payload)))

    with pytest.raises(AuthTokenRejectedError):
        await adapter.verify("signed-token")


@pytest.mark.asyncio
async def test_fails_closed_for_malformed_success_response() -> None:
    adapter = verifier(
        httpx.MockTransport(lambda _request: httpx.Response(200, json={"user_id": "user-1"}))
    )

    with pytest.raises(AuthVerifierUnavailableError):
        await adapter.verify("signed-token")


@pytest.mark.asyncio
async def test_rejects_malformed_bearer_token_without_network_call() -> None:
    def unexpected_call(_request: httpx.Request) -> httpx.Response:
        raise AssertionError("auth-core must not be called")

    adapter = verifier(httpx.MockTransport(unexpected_call))

    with pytest.raises(AuthTokenRejectedError):
        await adapter.verify("token with spaces")


@pytest.mark.asyncio
async def test_handoff_exchange_uses_server_credential_and_returns_token() -> None:
    async def handle(request: httpx.Request) -> httpx.Response:
        assert request.headers["X-Handoff-Client-Secret"] == "private-client-secret"
        assert request.url.path == "/api/v1/auth/handoff/exchange"
        return httpx.Response(
            200,
            json={"access_token": "signed-access-token-value", "token_type": "Bearer"},
        )

    http_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handle), base_url="http://auth-core:8000"
    )
    adapter = AuthCoreHandoffClient(
        base_url="http://unused",
        client_secret="private-client-secret",
        timeout_seconds=2,
        client=http_client,
    )

    token = await adapter.exchange(
        code="single-use-code", return_url="http://localhost:5173/auth/return"
    )

    assert token == "signed-access-token-value"


@pytest.mark.asyncio
async def test_handoff_exchange_maps_replayed_code_to_safe_rejection() -> None:
    http_client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _request: httpx.Response(400)),
        base_url="http://auth-core:8000",
    )
    adapter = AuthCoreHandoffClient(
        base_url="http://unused",
        client_secret="private-client-secret",
        timeout_seconds=2,
        client=http_client,
    )

    with pytest.raises(AuthHandoffRejectedError):
        await adapter.exchange(
            code="replayed-code", return_url="http://localhost:5173/auth/return"
        )
