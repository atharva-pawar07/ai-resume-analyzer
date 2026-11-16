import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
from datetime import datetime, timedelta, timezone
import jwt
from backend.app.core.security import SECRET_KEY, ALGORITHM



@pytest.mark.asyncio
async def test_root_endpoint():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        response = await client.get("/")

        assert response.status_code == 200

        data = response.json()

        assert data["message"] == "Welcome to AI Resume Analyzer API"
        assert data["status"] == "running"

@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        response = await client.get("/health")

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        response = await client.get("/health")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "healthy"
        assert data["application"] == "AI Resume Analyzer"


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "testuser@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    user_data = {
        "full_name": "Test User",
        "email": "duplicate@example.com",
        "password": "TestPassword123"
    }

    first_response = await client.post(
        "/api/v1/auth/register",
        json=user_data
    )

    second_response = await client.post(
        "/api/v1/auth/register",
        json=user_data
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email is already registered"


@pytest.mark.asyncio
async def test_login_user(client):
    user_data = {
        "full_name": "Login Test User",
        "email": "login@example.com",
        "password": "TestPassword123"
    }

    register_response = await client.post(
        "/api/v1/auth/register",
        json=user_data
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "TestPassword123"
        }
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert data["token_type"] == "bearer"
    assert "access_token" in data
    assert len(data["access_token"]) > 0

@pytest.mark.asyncio
async def test_login_invalid_password(client):
    user_data = {
        "full_name": "Invalid Login User",
        "email": "invalid@example.com",
        "password": "CorrectPassword123"
    }

    await client.post(
        "/api/v1/auth/register",
        json=user_data
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "invalid@example.com",
            "password": "WrongPassword123"
        }
    )

    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid email or password"

@pytest.mark.asyncio
async def test_get_current_user(client):
    user_data = {
        "full_name": "Profile Test User",
        "email": "profile@example.com",
        "password": "TestPassword123"
    }

    await client.post(
        "/api/v1/auth/register",
        json=user_data
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "profile@example.com",
            "password": "TestPassword123"
        }
    )

    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["full_name"] == "Profile Test User"
    assert response.json()["email"] == "profile@example.com"

@pytest.mark.asyncio
async def test_get_current_user_without_token(client):
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Invalid Email User",
            "email": "not-an-email",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Short Password User",
            "email": "shortpassword@example.com",
            "password": "12345"
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_unregistered_email(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


@pytest.mark.asyncio
async def test_get_current_user_with_invalid_token(client):
    response = await client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid.jwt.token"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


@pytest.mark.asyncio
async def test_get_current_user_with_expired_token(client):
    expired_token = jwt.encode(
        {
            "sub": "1",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response = await client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {expired_token}"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"