import asyncio
import httpx
import json

API_URL = "http://localhost:8000/chat"
USER_ID = "inspect_milk_user"

async def inspect():
    query = "milk price"
    print(f"Querying: {query}...")
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(API_URL, json={"text": query, "user_id": USER_ID}, timeout=60.0)
            if resp.status_code == 200:
                data = resp.json()
                print("\nResponse:")
                print(data.get("response", "")[:200] + "...")
                
                print("\nMetadata Images:")
                meta = data.get("metadata", [])
                for idx, m in enumerate(meta):
                    url = m.get("image_url", "NO_URL")
                    print(f"[{idx+1}] {url}")
            else:
                print(f"Error {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(inspect())
