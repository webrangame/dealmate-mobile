import asyncio
import os
from rag_engine import RAGEngine
import httpx

async def test_rag_message():
    # Setup test params
    litellm_api_base = os.getenv("LITELLM_API_BASE")
    litellm_api_key = os.getenv("LITELLM_API_KEY")
    test_user_id = f"test_user_rag_{int(asyncio.get_event_loop().time())}"

    print(f"Testing RAG message with user: {test_user_id}")
    
    # 1. Create user with 0 budget in LiteLLM directly
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{litellm_api_base}/user/new",
            headers={"x-litellm-api-key": litellm_api_key},
            json={
                "user_id": test_user_id,
                "max_budget": 0.0,
                "budget_duration": "daily"
            }
        )
        print("User created with 0 budget.")

    # 2. Call RAG Engine query
    engine = RAGEngine()
    print("Calling RAG engine...")
    try:
        result = await engine.query("What is the price of milk?", user_id=test_user_id)
        print(f"RAG Response: {result['response']}")
        if "token/budget limit is finished" in result['response']:
            print("✅ SUCCESS: User-friendly message received!")
        else:
            print("❌ FAILURE: Message not received as expected.")
    except Exception as e:
        print(f"Unexpected RAG error: {e}")

if __name__ == "__main__":
    asyncio.run(test_rag_message())
