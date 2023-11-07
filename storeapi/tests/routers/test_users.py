import pytest
from fastapi import status
from httpx import AsyncClient


async def register_user(async_client: AsyncClient, email: str, password: str):
    return await async_client.post(
        "/users/register/",
        json={"email": email, "password": password},
    )


async def login_user(async_client: AsyncClient, email: str, password: str):
    return await async_client.post(
        "/users/token/",
        json={"email": email, "password": password},
    )


@pytest.mark.anyio
async def test_register_user(async_client: AsyncClient):
    response = await register_user(async_client, "test@example.com", "1234")

    assert response.status_code == status.HTTP_201_CREATED
    assert "User created" in response.json()["detail"]


@pytest.mark.anyio
async def test_register_user_already_exists(
    async_client: AsyncClient, registered_user: dict
):
    response = await register_user(
        async_client, registered_user["email"], registered_user["password"]
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_login_user_not_exists(async_client: AsyncClient):
    response = await login_user(async_client, "test@example.com", "1234")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_login_user_invalid_password(
    async_client: AsyncClient, registered_user: dict
):
    response = await login_user(async_client, registered_user["email"], "wrong_pass")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_login_user_valid(async_client: AsyncClient, registered_user: dict):
    response = await login_user(
        async_client, registered_user["email"], registered_user["password"]
    )

    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response_data
    assert "token_type" in response_data
