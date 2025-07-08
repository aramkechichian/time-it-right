import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from app.schemas.auth import RegisterRequest, LoginRequest
from app.services import auth_service


@patch("app.services.auth_service.get_user_by_username")
@patch("app.services.auth_service.get_user_by_email")
@patch("app.services.auth_service.create_user")
@patch("app.services.auth_service.get_password_hash")
@patch("app.services.auth_service.create_access_token")
def test_register_user_success(mock_token, mock_hash, mock_create_user, mock_get_email, mock_get_username):
    mock_get_username.return_value = None
    mock_get_email.return_value = None
    mock_hash.return_value = "hashed"
    mock_user = MagicMock()
    mock_user.id = uuid4()
    mock_create_user.return_value = mock_user
    mock_token.return_value = "jwt_token"

    db = MagicMock()
    request = RegisterRequest(username="user", email="user@example.com", password="123456")

    token = asyncio.run(auth_service.register_user(db, request))

    assert token.access_token == "jwt_token"


@patch("app.services.auth_service.get_user_by_username")
@patch("app.services.auth_service.get_user_by_email")
def test_register_user_existing_username(mock_get_email, mock_get_username):
    mock_get_username.return_value = True
    mock_get_email.return_value = None
    db = MagicMock()
    request = RegisterRequest(username="user", email="user@example.com", password="123456")

    with pytest.raises(Exception):
        asyncio.run(auth_service.register_user(db, request))


@patch("app.services.auth_service.get_user_by_username")
@patch("app.services.auth_service.get_user_by_email")
def test_register_user_existing_email(mock_get_email, mock_get_username):
    mock_get_username.return_value = None
    mock_get_email.return_value = True
    db = MagicMock()
    request = RegisterRequest(username="user", email="taken@example.com", password="123456")

    with pytest.raises(Exception):
        asyncio.run(auth_service.register_user(db, request))


@patch("app.services.auth_service.get_user_by_username_or_email")
@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.create_access_token")
def test_login_user_success(mock_token, mock_verify, mock_get_user):
    fake_user = MagicMock()
    fake_user.id = uuid4()
    fake_user.hashed_password = "hashed"

    mock_get_user.return_value = fake_user
    mock_verify.return_value = True
    mock_token.return_value = "jwt_token"

    db = MagicMock()
    request = LoginRequest(username_or_email="testuser", password="password")

    token = asyncio.run(auth_service.login_user(db, request))

    assert token.access_token == "jwt_token"


@patch("app.services.auth_service.get_user_by_username_or_email")
@patch("app.services.auth_service.verify_password")
def test_login_user_invalid_credentials(mock_verify, mock_get_user):
    mock_get_user.return_value = None
    mock_verify.return_value = False

    db = MagicMock()
    request = LoginRequest(username_or_email="notfound", password="wrong")

    with pytest.raises(Exception):
        asyncio.run(auth_service.login_user(db, request))
