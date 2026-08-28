import pytest
from httpx import AsyncClient

from src.database.models import User
from src.main import app
from src.services.auth_service import get_password_hash, verify_password


@pytest.mark.asyncio
async def test_oauth_password_unpredictable(db_session):
    """Test user created via OAuth gets an unpredictable password."""
    # Create an OAuth user directly
    import secrets
    email = "oauth.user@example.com"
    user = User(
        email=email,
        full_name="OAuth User",
        password_hash=get_password_hash(secrets.token_urlsafe(32)),
        role="CUSTOMER",
        status="ACTIVE",
    )
    db_session.add(user)
    await db_session.commit()

    # Verify they cannot log in with the predictable password gauth_<email>
    predictable_password = f"gauth_{email}"
    assert verify_password(predictable_password, user.password_hash) is False

    # Also test the login endpoint
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": predictable_password}
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.text
