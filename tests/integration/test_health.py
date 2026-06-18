"""Tests d'intégration — health check et routes de base."""

from httpx import AsyncClient


async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


async def test_openapi_json_disponible(client: AsyncClient) -> None:
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "components" in schema


async def test_docs_disponible(client: AsyncClient) -> None:
    response = await client.get("/docs")
    assert response.status_code == 200