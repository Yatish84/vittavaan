"""Browser-bound start and server-side exchange for auth-core handoff."""

from urllib.parse import parse_qs, urlsplit

import pytest
from httpx import ASGITransport, AsyncClient
from vittavaan.boundary.api import create_app
from vittavaan.config import Settings


class FakeHandoffClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    async def exchange(self, *, code: str, return_url: str) -> str:
        self.calls.append((code, return_url))
        return "signed-access-token-value"


def build_app():
    settings = Settings(
        APP_ENV="test",
        APP_RELEASE_ID="test-release",
        DATABASE_URL="postgresql+asyncpg://user:secret@localhost/test",
        REDIS_URL="redis://:secret@localhost:6379/0",
    )
    app = create_app(settings)
    handoff = FakeHandoffClient()
    app.state.auth_core_handoff = handoff
    return app, handoff


@pytest.mark.asyncio
async def test_handoff_start_sets_http_only_state_without_a_token() -> None:
    app, _handoff = build_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/auth/handoff/start")

    assert response.status_code == 200
    authorization_url = response.json()["authorization_url"]
    query = parse_qs(urlsplit(authorization_url).query)
    assert query["return_url"] == ["http://localhost:5173/auth/return"]
    assert len(query["state"][0]) >= 32
    assert "access_token" not in authorization_url
    assert "HttpOnly" in response.headers["set-cookie"]
    assert response.headers["cache-control"] == "no-store"


@pytest.mark.asyncio
async def test_handoff_exchange_requires_matching_browser_state() -> None:
    app, handoff = build_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        start = await client.post("/api/v1/auth/handoff/start")
        state = parse_qs(urlsplit(start.json()["authorization_url"]).query)["state"][0]
        response = await client.post(
            "/api/v1/auth/handoff/exchange",
            json={"code": "single-use-code-with-enough-characters", "state": state},
        )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "signed-access-token-value",
        "token_type": "Bearer",
    }
    assert handoff.calls == [
        (
            "single-use-code-with-enough-characters",
            "http://localhost:5173/auth/return",
        )
    ]
    assert response.headers["cache-control"] == "no-store"
    assert "Max-Age=0" in response.headers["set-cookie"]


@pytest.mark.asyncio
async def test_handoff_exchange_rejects_state_mismatch_before_auth_core_call() -> None:
    app, handoff = build_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/api/v1/auth/handoff/start")
        response = await client.post(
            "/api/v1/auth/handoff/exchange",
            json={
                "code": "single-use-code-with-enough-characters",
                "state": "wrong-state-with-at-least-thirty-two-characters",
            },
        )

    assert response.status_code == 400
    assert handoff.calls == []
