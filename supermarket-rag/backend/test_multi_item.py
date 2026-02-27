import asyncio
import os
from dotenv import load_dotenv
from rag_engine import RAGEngine

async def test_multi_item():
    load_dotenv()
    engine = RAGEngine()
    
    query = "i need buy ice cream 1l and rice 1 kg"
    print(f"Testing Query: {query}")
    
    response = await engine.query(query, user_id="test_user")
    
    print("\n--- RESPONSE ---")
    print(response.get("response"))
    print("\n--- METADATA COUNT ---")
    print(len(response.get("metadata", [])))
    
    if len(response.get("metadata", [])) == 0:
        print("\nWARNING: No products found in metadata!")
    else:
        print("\nProducts found in metadata:")
        for m in response.get("metadata", []):
            print(f"- {m.get('shop_name')}: {m.get('product_name')} ({m.get('price')})")

if __name__ == "__main__":
    asyncio.run(test_multi_item())
