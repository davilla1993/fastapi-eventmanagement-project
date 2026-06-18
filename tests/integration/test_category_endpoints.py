"""Tests d'intégration — endpoints Categories."""

from httpx import AsyncClient

_CATEGORIES_URL = "/api/v1/categories"


def _cat_payload(slug: str = "jazz") -> dict[str, object]:
    return {"name": slug.capitalize(), "slug": slug, "color": "#F59E0B"}


async def test_list_categories_public(client: AsyncClient) -> None:
    response = await client.get(_CATEGORIES_URL)
    assert response.status_code == 200
    assert "items" in response.json()


async def test_create_category_sans_auth(client: AsyncClient) -> None:
    response = await client.post(_CATEGORIES_URL, json=_cat_payload("noauth-cat"))
    assert response.status_code == 401


async def test_create_category_succes(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        _CATEGORIES_URL,
        json=_cat_payload("blues"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["slug"] == "blues"


async def test_get_category_introuvable(client: AsyncClient) -> None:
    response = await client.get(
        f"{_CATEGORIES_URL}/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404


async def test_create_category_couleur_invalide(
    client: AsyncClient, admin_token: str
) -> None:
    payload = _cat_payload("rock")
    payload["color"] = "rouge"
    response = await client.post(
        _CATEGORIES_URL,
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 422


async def test_pagination_categories(client: AsyncClient) -> None:
    response = await client.get(f"{_CATEGORIES_URL}?page=1&size=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 5