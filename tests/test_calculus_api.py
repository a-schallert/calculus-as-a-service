import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_optimize():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/optimize", json={
            "function": "100*x - 2*x**2",
            "variable": "x",
            "domain": [0, 50]
        })
    data = response.json()
    assert response.status_code == 200
    assert data["at_x"] == 25.0
    assert data["max_value"] == 1250.0

@pytest.mark.asyncio
async def test_derivative():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/derivative", json={
            "function": "3*x**2 + 2*x",
            "variable": "x",
            "order": 1,
            "at_point": 4
        })
    data = response.json()
    assert response.status_code == 200
    assert data["value"] == 26.0

@pytest.mark.asyncio
async def test_integrate():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/integrate", json={
            "function": "3*x**2",
            "variable": "x",
            "lower_bound": 0,
            "upper_bound": 5
        })
    data = response.json()
    assert response.status_code == 200
    assert data["result"] == 125.0

@pytest.mark.asyncio
async def test_gradient():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/gradient", json={
            "function": "x**2 * y + y**2",
            "variables": ["x", "y"],
            "at_point": {"x": 1, "y": 2}
        })
    data = response.json()
    assert response.status_code == 200
    assert data["value"] == [4.0, 5.0]