import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.database.models import User, UserRole, UserStatus
from src.main import app
from src.services.auth_service import get_password_hash


@pytest.mark.asyncio
async def test_sale_endpoint_requires_sale_role(db_session):
    """Test a customer gets 403 when accessing a SALE-only endpoint."""
    customer = User(
        email="customer.role.test@example.com",
        full_name="Customer User",
        password_hash=get_password_hash("password"),
        role=UserRole.CUSTOMER,
        status=UserStatus.ACTIVE,
    )
    db_session.add(customer)
    await db_session.commit()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # First login to get token
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": customer.email, "password": "password"}
        )
        token = response.json()["access_token"]
        
        # Access a sale endpoint
        res = await client.get(
            "/api/v1/sale/overview",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res.status_code == 403


@pytest.mark.asyncio
async def test_admin_endpoint_requires_admin_role(db_session):
    """Test a customer gets 403 when accessing an ADMIN-only endpoint."""
    customer = User(
        email="customer.admin.test@example.com",
        full_name="Customer User",
        password_hash=get_password_hash("password"),
        role=UserRole.CUSTOMER,
        status=UserStatus.ACTIVE,
    )
    db_session.add(customer)
    await db_session.commit()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # First login to get token
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": customer.email, "password": "password"}
        )
        token = response.json()["access_token"]
        
        # Assuming there is an admin endpoint, for example /admin/users (if it exists)
        # Using a mock endpoint here to represent it
        app_mock = FastAPI()
        from src.api.routes.auth import require_roles
        from fastapi import Depends
        
        @app_mock.get("/admin/test")
        async def admin_only(user: User = Depends(require_roles(UserRole.ADMIN))):
            return {"ok": True}
        
        # Need to include the auth dependency context properly.
        # Let's just test that the dependency function throws 403.
        from src.api.routes.auth import require_roles
        from fastapi import HTTPException
        
        dependency = require_roles(UserRole.ADMIN)
        try:
            await dependency(user=customer)
            assert False, "Should have raised 403"
        except HTTPException as e:
            assert e.status_code == 403


@pytest.mark.asyncio
async def test_unauthenticated_access_returns_401():
    """Test accessing protected endpoints without a token returns 401."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        res = await client.get("/api/v1/sale/overview")
        assert res.status_code == 401
