"""Tests d'intégration — endpoints Venues."""

from httpx import AsyncClient

_VENUES_URL = "/api/v1/venues"


def _venue_payload(slug_suffix: str = "") -> dict[str, object]:
    return {
        "name": f"Salle Test{slug_suffix}",
        "slug": f"salle-test{slug_suffix}",
        "address": "1 Rue de la Paix",
        "city": "Paris",
        "postal_code": "75001",
        "capacity": 500,
    }


async def test_list_venues_public(client: AsyncClient) -> None:
    response = await client.get(_VENUES_URL)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


async def test_create_venue_sans_auth(client: AsyncClient) -> None:
    response = await client.post(_VENUES_URL, json=_venue_payload("noauth"))
    assert response.status_code == 401


async def test_create_venue_succes(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        _VENUES_URL,
        json=_venue_payload("-create-ok"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Salle Test-create-ok"
    assert data["city"] == "Paris"
    assert "public_id" in data


async def test_create_venue_slug_duplique(client: AsyncClient, admin_token: str) -> None:
    payload = _venue_payload("-dup")
    await client.post(
        _VENUES_URL, json=payload, headers={"Authorization": f"Bearer {admin_token}"}
    )
    response = await client.post(
        _VENUES_URL, json=payload, headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 409


async def test_get_venue_introuvable(client: AsyncClient) -> None:
    response = await client.get(f"{_VENUES_URL}/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


async def test_list_venues_filtre_city(client: AsyncClient) -> None:
    response = await client.get(f"{_VENUES_URL}?city=Paris")
    assert response.status_code == 200


async def test_create_venue_postal_invalide(
    client: AsyncClient, admin_token: str
) -> None:
    payload = _venue_payload("-bad-postal")
    payload["postal_code"] = "99999"
    response = await client.post(
        _VENUES_URL, json=payload, headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 422