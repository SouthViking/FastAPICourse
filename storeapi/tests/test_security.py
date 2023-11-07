import pytest
from fastapi import HTTPException
from jose import jwt

from storeapi import security


def test_access_token_expire_minutes():
    assert security.access_token_expire_minutes() == 30


def test_create_access_token():
    expected_sub = "123"

    token = security.create_access_token(expected_sub)

    decoded_token = jwt.decode(
        token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
    )

    assert "sub" in decoded_token
    assert decoded_token["sub"] == expected_sub
    assert "exp" in decoded_token


def test_password_hashes():
    password = "password"
    assert security.verify_password(password, security.get_password_hash(password))


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await security.get_user(registered_user["email"])

    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await security.get_user("text@example.com")

    assert user is None, "None should be returned when the user does not exist."


@pytest.mark.anyio
async def test_get_current_user_from_token(registered_user: dict):
    access_token = security.create_access_token(registered_user["email"])
    user = await security.get_user_from_token(access_token)

    assert user["email"] == registered_user["email"]


@pytest.mark.anyio
async def test_get_current_user_from_invalid_token():
    with pytest.raises(HTTPException):
        await security.get_user_from_token("invalid token")
