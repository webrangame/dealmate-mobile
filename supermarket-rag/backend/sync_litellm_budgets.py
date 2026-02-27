import httpx
import psycopg2
import os
import asyncio
from dotenv import load_dotenv

async def sync_budgets():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    # In this environment, LITELLM_API_KEY is used as the master key for proxy admin
    litellm_api_key = os.getenv("LITELLM_API_KEY") 
    litellm_api_base = os.getenv("LITELLM_API_BASE")
    
    if not all([db_url, litellm_api_key, litellm_api_base]):
        print(f"Missing environment variables: DB={bool(db_url)}, KEY={bool(litellm_api_key)}, BASE={bool(litellm_api_base)}")
        return

    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        cur = conn.cursor()
        
        # Fetch all users who have a LiteLLM user ID
        cur.execute("SELECT id, email, litellm_user_id FROM users WHERE litellm_user_id IS NOT NULL")
        users = cur.fetchall()
        
        print(f"Syncing budgets for {len(users)} users...")
        
        async with httpx.AsyncClient() as client:
            for db_id, email, litellm_user_id in users:
                print(f"Updating budget for user {db_id} (LiteLLM ID: {litellm_user_id})...")
                
                try:
                    # LiteLLM /user/update endpoint
                    # Re-enforces budget of $0.25 (approx 5M tokens)
                    response = await client.post(
                        f"{litellm_api_base}/user/update",
                        headers={"x-litellm-api-key": litellm_api_key},
                        json={
                            "user_id": litellm_user_id,
                            "max_budget": 0.25
                        },
                        timeout=10.0
                    )
                    
                    if response.status_code == 200:
                        print(f"✅ Successfully updated user {litellm_user_id}")
                    else:
                        print(f"❌ Failed to update user {litellm_user_id}: {response.status_code} - {response.text}")
                except Exception as e:
                    print(f"❌ Error updating user {litellm_user_id}: {e}")
        
        cur.close()
        conn.close()
        print("Budget synchronization complete!")
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    asyncio.run(sync_budgets())
