import asyncio
import os
from rag_engine import rag_engine

async def test_get_items():
    print("Testing get_shop_items for 'Coles'...")
    items = await rag_engine.get_shop_items("Coles")
    print(f"Found {len(items)} items for Coles.")
    if items:
        print(f"Sample item: {items[0]}")
    
    print("\nTesting get_shop_items for 'Woolworths'...")
    items = await rag_engine.get_shop_items("Woolworths")
    print(f"Found {len(items)} items for Woolworths.")
    if items:
        print(f"Sample item: {items[0]}")

if __name__ == "__main__":
    asyncio.run(test_get_items())
