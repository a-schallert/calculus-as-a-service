import asyncio
import httpx

BASE_URL = "http://localhost:8000"

async def test_all_endpoints():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:

        print("\n--- Testing /optimize ---")
        res = await client.post("/optimize", json={
            "function": "100*x - 2*x**2",
            "variable": "x",
            "domain": [0, 50]
        })
        print(res.json())

        print("\n--- Testing /derivative ---")
        res = await client.post("/derivative", json={
            "function": "3*x**2 + 2*x",
            "variable": "x",
            "order": 1,
            "at_point": 4
        })
        print(res.json())

        print("\n--- Testing /integrate ---")
        res = await client.post("/integrate", json={
            "function": "3*x**2",
            "variable": "x",
            "lower_bound": 0,
            "upper_bound": 5
        })
        print(res.json())

        print("\n--- Testing /rate-of-change ---")
        res = await client.post("/rate-of-change", json={
            "function": "100*x - 2*x**2",
            "variable": "x",
            "at_point": 25,
            "context": "profit"
        })
        print(res.json())

        print("\n--- Testing /critical-points ---")
        res = await client.post("/critical-points", json={
            "function": "x**3 - 3*x**2 + 2",
            "variable": "x"
        })
        print(res.json())

        print("\n--- Testing /partial-derivative ---")
        res = await client.post("/partial-derivative", json={
            "function": "x**2 * y + sin(y)",
            "variables": ["x", "y"],
            "respect_to": "x",
            "at_point": {"x": 2, "y": 1}
        })
        print(res.json())

        print("\n--- Testing /gradient ---")
        res = await client.post("/gradient", json={
            "function": "x**2 * y + y**2",
            "variables": ["x", "y"],
            "at_point": {"x": 1, "y": 2}
        })
        print(res.json())

if __name__ == "__main__":
    asyncio.run(test_all_endpoints())
