import httpx
import asyncio
import json

async def q():
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post('http://localhost:8000/chat', json={
            'text': 'compare milk prices between coles and woolworths',
            'user_id': 'itranga@gmail.com'
        })
        print(f"Status: {resp.status_code}")
        print("Response:")
        print(resp.json().get('response', 'No response'))

if __name__ == "__main__":
    asyncio.run(q())
