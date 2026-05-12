"""Tests for the health check endpoint."""

import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """GET /api/health should return success."""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "success"
    assert data["data"]["status"] == "ok"
    assert "app_name" in data["data"]
    assert "version" in data["data"]


@pytest.mark.asyncio
async def test_health_response_format(client):
    """Health check response should include timestamp."""
    response = await client.get("/api/health")
    data = response.json()
    assert "timestamp" in data
    assert data["timestamp"] != ""
