from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from src.api.routes.auth import require_roles
from src.database.models import UserRole
from src.main import app


def _user(role: UserRole):
    return SimpleNamespace(id="00000000-0000-0000-0000-000000000001", role=role)


@pytest.mark.asyncio
async def test_customer_is_rejected_from_sale_endpoints():
    """A customer hitting a SALE-only dependency must get 403, not data."""
    dependency = require_roles(UserRole.SALE)

    with pytest.raises(HTTPException) as exc:
        await dependency(user=_user(UserRole.CUSTOMER))

    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_customer_is_rejected_from_admin_endpoints():
    dependency = require_roles(UserRole.ADMIN)

    with pytest.raises(HTTPException) as exc:
        await dependency(user=_user(UserRole.CUSTOMER))

    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_sale_cannot_reach_admin_endpoints():
    """Sale is privileged but still not an admin."""
    dependency = require_roles(UserRole.ADMIN)

    with pytest.raises(HTTPException) as exc:
        await dependency(user=_user(UserRole.SALE))

    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_matching_role_passes_through():
    """The guard must not block the role it is meant to allow."""
    dependency = require_roles(UserRole.SALE, UserRole.ADMIN)

    user = _user(UserRole.SALE)
    assert await dependency(user=user) is user


@pytest.mark.asyncio
async def test_unauthenticated_access_returns_401():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/sale/overview")

    assert res.status_code == 401
