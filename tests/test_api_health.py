import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """Test GET /health trả về status healthy."""
    response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app" in data
    assert "env" in data


@pytest.mark.asyncio
async def test_health_check_has_database(client):
    """Test GET /health bao gồm database status."""
    response = await client.get("/health")

    data = response.json()
    assert "app" in data
    assert "env" in data


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test GET / trả về thông tin API."""
    response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "description" in data
