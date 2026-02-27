import asyncio
import os
from dotenv import load_dotenv
from rag_engine import RAGEngine

async def test_search(engine, query_text):
    user_id = "local_verifier"
    print(f"\n>>> TESTING QUERY: '{query_text}'")
    result = await engine.query(query_text, user_id=user_id)
    
    print("-" * 30)
    print("RESPONSE:")
    print(result.get("response"))
    print("-" * 30)
    
    metadata = result.get("metadata", [])
    print(f"IMAGES FOUND: {len(metadata)}")
    for i, m in enumerate(metadata):
        print(f"  {i+1}. {m.get('shop_name')} | {m.get('product_name')} | {m.get('price')}")

async def main():
    load_dotenv()
    print("Initialising RAGEngine...")
    engine = RAGEngine()
    
    # Test 1: Solid fix for 'rice' collision
    await test_search(engine, "is there rice")
    
    # Test 2: Handling of general 'price' queries
    await test_search(engine, "i need price")

if __name__ == "__main__":
    asyncio.run(main())
