import asyncio
import json
import httpx

async def check():
    url = "http://localhost:8000/chat"
    payload = {
        "text": "i need to eat ice cream today",
        "user_id": "test_verification"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            data = resp.json()
            images = data.get("metadata", [])
            print(f"Local API images: {len(images)}")
            for i in images:
                print(f" - {i.get('product_name')}")
    except Exception as e:
        print(f"Local API error: {e}")

    url_prod = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url_prod, json=payload)
            data = resp.json()
            images = data.get("metadata", [])
            print(f"Prod API images: {len(images)}")
            for i in images:
                print(f" - {i.get('product_name')}")
    except Exception as e:
        print(f"Prod API error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
