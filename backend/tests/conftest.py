"""
pytest configuration and shared fixtures for BridgeWatch AI backend tests.
"""

import asyncio

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.database import Base, async_session_factory
from app.main import app
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.id_generator import IDGenerator


@pytest.fixture(scope="session")
def event_loop():
    """Create a single event loop for the entire test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """Create all tables and seed default users before any tests."""
    async with async_session_factory() as db:
        # Create users table explicitly
        from app.database import engine
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Seed default users
        for u in [
            {"username": "admin", "password": "admin123", "display_name": "Admin", "role": "admin"},
            {"username": "operator", "password": "operator123", "display_name": "Operator", "role": "operator"},
            {"username": "viewer", "password": "viewer123", "display_name": "Viewer", "role": "viewer"},
        ]:
            existing = await db.execute(select(User).where(User.username == u["username"]))
            if not existing.scalar_one_or_none():
                db.add(User(
                    user_id=IDGenerator.generate("USR"),
                    username=u["username"],
                    hashed_password=AuthService.hash_password(u["password"]),
                    display_name=u["display_name"],
                    role=u["role"],
                    is_active=True,
                ))
        await db.commit()


@pytest_asyncio.fixture(scope="session")
async def client():
    """Provide an HTTP client against the FastAPI app (ASGI, no network)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="session")
async def auth_headers(client) -> dict:
    """Login as admin and return JWT auth headers."""
    response = await client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
