import httpx
import asyncio
import os

async def get_litellm_info(user_id):
    api_base = "https://swzissb82u.us-east-1.awsapprunner.com"
    master_key = "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{api_base}/user/info?user_id={user_id}",
            headers={"x-litellm-api-key": master_key}
        )
        print(f"Status: {resp.status_code}")
        print(f"Data: {resp.text}")

if __name__ == "__main__":
    target = "832c18aca270e07e169cf8e03d605b550873147671d649114c95bcee0af75e06"
    asyncio.run(get_litellm_info(target))
