"""Tests for the authentication endpoints."""

import pytest


@pytest.mark.asyncio
async def test_login_success(client, auth_headers):
    """Login with valid credentials should return a token."""
    # We use the test user created in conftest
    response = await client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["access_token"] != ""
    assert data["data"]["token_type"] == "bearer"
    assert data["data"]["role"] == "admin"
    assert data["data"]["username"] == "admin"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """Login with wrong password should return 401."""
    response = await client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == 401


@pytest.mark.asyncio
async def test_login_wrong_username(client):
    """Login with non-existent user should return 401."""
    response = await client.post(
        "/api/auth/login",
        json={"username": "nonexistent", "password": "admin123"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_no_auth(client):
    """Accessing protected endpoint without token should return 401."""
    response = await client.get("/api/events")
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == 401


@pytest.mark.asyncio
async def test_protected_endpoint_with_auth(client, auth_headers):
    """Accessing protected endpoint with valid token should succeed."""
    response = await client.get("/api/events", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0


@pytest.mark.asyncio
async def test_get_me(client, auth_headers):
    """GET /api/auth/me should return current user info."""
    response = await client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "admin"
    assert data["data"]["role"] == "admin"
