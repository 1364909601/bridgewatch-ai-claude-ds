from fastapi import Header
from typing import Optional

# Phase 2: soft auth — always returns default admin user.
# Phase 3+: validate JWT from Authorization header and return real user context.


async def get_current_user(
    authorization: Optional[str] = Header(None),
) -> dict:
    return {
        "user_id": "admin-001",
        "username": "admin",
        "role": "admin",
    }
