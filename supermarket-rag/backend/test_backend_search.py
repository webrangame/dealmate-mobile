import asyncio
from rag_engine import rag_engine

async def test_search():
    print("Testing search for Coles...")
    # Test 1: No search
    items = await rag_engine.get_shop_items("Coles", limit=5)
    print(f"Total items (no search): {len(items)}")
    
    # Test 2: Search for 'milk'
    items_milk = await rag_engine.get_shop_items("Coles", search="milk", limit=5)
    print(f"Items with search 'milk': {len(items_milk)}")
    for item in items_milk:
        print(f"- {item['product']}")

if __name__ == "__main__":
    asyncio.run(test_search())
