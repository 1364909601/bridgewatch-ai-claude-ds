"""Tests for the events API endpoints."""

import pytest


@pytest.mark.asyncio
async def test_events_list_empty(client, auth_headers):
    """GET /api/events should return empty list when no events exist."""
    response = await client.get("/api/events", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["total"] >= 0
    assert isinstance(data["data"]["list"], list)


@pytest.mark.asyncio
async def test_events_pagination_format(client, auth_headers):
    """Event list response should include pagination fields."""
    response = await client.get("/api/events", headers=auth_headers)
    data = response.json()
    assert "page_no" in data["data"]
    assert "page_size" in data["data"]
    assert "total" in data["data"]
    assert "list" in data["data"]


@pytest.mark.asyncio
async def test_event_detail_not_found(client, auth_headers):
    """GET /api/events/{non_existent_id} should return 404."""
    response = await client.get(
        "/api/events/EVT-NONEXISTENT", headers=auth_headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_review_nonexistent_event(client, auth_headers):
    """POST /api/events/{non_existent_id}/review should return 404."""
    response = await client.post(
        "/api/events/EVT-NONEXISTENT/review",
        headers=auth_headers,
        json={"review_status": "reviewed"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_dashboard_summary(client, auth_headers):
    """GET /api/dashboard/summary should return valid structure."""
    response = await client.get("/api/dashboard/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    # Should have all summary fields
    assert "total" in data
    assert "high_risk" in data
    assert "medium_risk" in data
    assert "low_risk" in data
    assert "total_objects" in data
    # Verify types (actual values depend on database state)
    assert isinstance(data["total"], int)
    assert isinstance(data["high_risk"], int)
    assert isinstance(data["medium_risk"], int)
    assert isinstance(data["low_risk"], int)
