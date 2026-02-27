import httpx
import os
import asyncio
import json
from dotenv import load_dotenv

async def check():
    load_dotenv()
    litellm_api_base = os.getenv("LITELLM_API_BASE")
    litellm_api_key = os.getenv("LITELLM_API_KEY")
    
    user_id = "6769c408ff3264dfd8ea1256d10787afe00eefac67426d78f839e6789912f567"
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{litellm_api_base}/user/info?user_id={user_id}",
                headers={"x-litellm-api-key": litellm_api_key}
            )
            print(json.dumps(resp.json(), indent=2))
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
