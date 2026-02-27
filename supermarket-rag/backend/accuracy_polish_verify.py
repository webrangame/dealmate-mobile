import asyncio
import os
from dotenv import load_dotenv
from rag_engine import RAGEngine

async def test_search(engine, query_text):
    user_id = "accuracy_polish_tester"
    print(f"\n>>> TESTING QUERY: '{query_text}'")
    result = await engine.query(query_text, user_id=user_id)
    
    print("-" * 30)
    print("RESPONSE:")
    print(result.get("response")[:500] + "...") # Truncate for brevity
    print("-" * 30)
    
    metadata = result.get("metadata", [])
    print(f"IMAGES FOUND: {len(metadata)}")
    for i, m in enumerate(metadata[:5]):
        print(f"  {i+1}. {m.get('shop_name')} | {m.get('product_name')} | {m.get('price')}")

async def main():
    load_dotenv()
    print("Initialising RAGEngine...")
    engine = RAGEngine()
    
    # Test normalization: plural search should hit singular DB entry
    await test_search(engine, "Price of eggs")
    await test_search(engine, "Price of Tim Tams")
    
    # Re-verify rice (word boundary)
    await test_search(engine, "is there rice")

if __name__ == "__main__":
    asyncio.run(main())
