import asyncio
import httpx

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"

async def test_hello():
    print(f"Testing Basic Chat: {API_URL}")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                API_URL, 
                json={"text": "Hello", "user_id": "test_hello"}, 
                timeout=30.0
            )
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_hello())
