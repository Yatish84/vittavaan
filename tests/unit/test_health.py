import pytest
from httpx import ASGITransport, AsyncClient
from vittavaan.boundary.api import create_app
from vittavaan.config import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings(
        APP_ENV="test",
        APP_RELEASE_ID="test-release",
        DATABASE_URL="postgresql+asyncpg://user:secret@localhost/test",
        REDIS_URL="redis://:secret@localhost:6379/0",
    )


@pytest.mark.asyncio
async def test_liveness_is_safe_and_correlated(settings: Settings) -> None:
    app = create_app(settings)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "live", "release_id": "test-release"}
    assert response.headers["X-Correlation-ID"]
    assert "secret" not in response.text


@pytest.mark.asyncio
async def test_unknown_route_returns_safe_problem_details(settings: Settings) -> None:
    app = create_app(settings)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json() == {
        "type": "urn:vittavaan:problem:not-found",
        "title": "Resource not found",
        "status": 404,
        "detail": "The requested resource does not exist.",
        "instance": "/does-not-exist",
    }
    assert "secret" not in response.text
