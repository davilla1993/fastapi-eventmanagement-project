"""Tests d'intégration — authentification."""

from httpx import AsyncClient

_REGISTER_URL = "/api/v1/auth/register"
_LOGIN_URL = "/api/v1/auth/login"
_ME_URL = "/api/v1/auth/me"


async def test_register_succes(client: AsyncClient) -> None:
    payload = {
        "full_name": "Test User Integ",
        "email": "testuser_integ@example.com",
        "password": "SecurePass123!",
    }
    response = await client.post(_REGISTER_URL, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "public_id" in data


async def test_register_email_duplique(client: AsyncClient) -> None:
    payload = {
        "full_name": "Dup User",
        "email": "dup@example.com",
        "password": "SecurePass123!",
    }
    await client.post(_REGISTER_URL, json=payload)
    response = await client.post(_REGISTER_URL, json=payload)
    assert response.status_code == 409


async def test_login_succes(client: AsyncClient) -> None:
    payload = {
        "full_name": "Login User",
        "email": "loginuser@example.com",
        "password": "SecurePass123!",
    }
    await client.post(_REGISTER_URL, json=payload)

    response = await client.post(
        _LOGIN_URL,
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_mauvais_mot_de_passe(client: AsyncClient) -> None:
    payload = {
        "full_name": "Bad Pass User",
        "email": "badpass@example.com",
        "password": "CorrectPass123!",
    }
    await client.post(_REGISTER_URL, json=payload)

    response = await client.post(
        _LOGIN_URL,
        json={"email": payload["email"], "password": "WrongPass!"},
    )
    assert response.status_code == 401


async def test_me_sans_token(client: AsyncClient) -> None:
    response = await client.get(_ME_URL)
    assert response.status_code == 401


async def test_me_avec_token(client: AsyncClient) -> None:
    payload = {
        "full_name": "Me User",
        "email": "meuser@example.com",
        "password": "SecurePass123!",
    }
    await client.post(_REGISTER_URL, json=payload)
    login = await client.post(
        _LOGIN_URL,
        json={"email": payload["email"], "password": payload["password"]},
    )
    token = login.json()["access_token"]

    response = await client.get(_ME_URL, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == payload["email"]