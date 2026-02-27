import httpx
import os
import asyncio
import json
from dotenv import load_dotenv

async def test_enforcement():
    load_dotenv()
    litellm_api_base = os.getenv("LITELLM_API_BASE")
    litellm_api_key = os.getenv("LITELLM_API_KEY")
    
    test_user_id = f"test_user_{os.urandom(4).hex()}"
    print(f"Testing with user: {test_user_id}")
    
    async with httpx.AsyncClient() as client:
        # 1. Create user with tiny budget
        print("Creating user with tiny budget ($0.00001)...")
        create_resp = await client.post(
            f"{litellm_api_base}/user/new",
            headers={"x-litellm-api-key": litellm_api_key},
            json={
                "user_id": test_user_id,
                "max_budget": 0.00001 # Extremely small budget
            }
        )
        print(f"User create status: {create_resp.status_code}")
        
        # 2. Generate key for user
        print("Generating key with tiny budget ($0.00001)...")
        key_resp = await client.post(
            f"{litellm_api_base}/key/generate",
            headers={"x-litellm-api-key": litellm_api_key},
            json={
                "user_id": test_user_id,
                "max_budget": 0.0,
                "budget_duration": "daily"

            }
        )
        # ... and user update/create
        await client.post(
            f"{litellm_api_base}/user/update", # or new, if it exists
            headers={"x-litellm-api-key": litellm_api_key},
            json={
                "user_id": test_user_id,
                "max_budget": 0.0,
                "budget_duration": "daily"

            }
        )


        key_data = key_resp.json()
        virtual_key = key_data.get("key")
        print(f"Generated key: {virtual_key}")
        
        if not virtual_key:
            print("Failed to generate key")
            return

        # 3. Try to use the key
        print("Making request with new key...")
        try:
            chat_resp = await client.post(
                f"{litellm_api_base}/chat/completions",
                headers={"Authorization": f"Bearer {virtual_key}"},
                json={
                    "model": "gemini-2.0-flash",
                    "messages": [{"role": "user", "content": "hi"}]
                },
                timeout=30.0
            )

            print(f"Chat response status: {chat_resp.status_code}")
            print(f"Response: {chat_resp.text}")
            
            if chat_resp.status_code == 429 or "budget" in chat_resp.text.lower():
                print("✅ Budget enforcement WORKED (Blocked with 429/Budget error)")
            else:
                print("⚠️ Request went through. Might need more usage to trigger.")
                
                # Try second request
                print("Waiting 10s for spend to propagate...")
                await asyncio.sleep(10)
                print("Making second request...")

                chat_resp2 = await client.post(
                    f"{litellm_api_base}/chat/completions",
                    headers={"Authorization": f"Bearer {virtual_key}"},
                    json={
                        "model": "gemini-2.0-flash",
                        "messages": [{"role": "user", "content": "tell me a long story"}]
                    },

                    timeout=30.0
                )
                print(f"Second chat response status: {chat_resp2.status_code}")
                print(f"Second response: {chat_resp2.text}")
                
                if chat_resp2.status_code == 429 or "budget" in chat_resp2.text.lower():
                    print("✅ Budget enforcement WORKED on second attempt")
                else:
                    print("❌ Budget enforcement FAILED or not triggered yet")

        except Exception as e:
            print(f"Error during chat: {e}")

if __name__ == "__main__":
    asyncio.run(test_enforcement())
