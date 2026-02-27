import asyncio
import os
import json
from rag_engine import rag_engine

async def reproduce():
    query = "i like eat ice cream today"
    user_id = "reproduce_user_123"
    
    print(f"Query 1: '{query}'")
    result1 = await rag_engine.query(query, user_id)
    
    print("\n--- RESPONSE 1 ---")
    print(result1['response'])
    print("\n--- METADATA 1 (Images) ---")
    for m in result1['metadata']:
        print(f"- {m.get('shop_name')}: {m.get('product_name')} | {m.get('image_url')}")
    
    print("\n" + "="*50 + "\n")
    
    print(f"Query 2: '{query}'")
    result2 = await rag_engine.query(query, user_id)
    
    print("\n--- RESPONSE 2 ---")
    print(result2['response'])
    print("\n--- METADATA 2 (Images) ---")
    for m in result2['metadata']:
        print(f"- {m.get('shop_name')}: {m.get('product_name')} | {m.get('image_url')}")

    # Compare responses
    if result1['response'] == result2['response']:
        print("\n✅ Responses are identical.")
    else:
        print("\n❌ Responses are DIFFERENT.")
        
    # Compare metadata
    if result1['metadata'] == result2['metadata']:
        print("✅ Metadata is identical.")
    else:
        print("❌ Metadata is DIFFERENT.")

if __name__ == "__main__":
    asyncio.run(reproduce())
