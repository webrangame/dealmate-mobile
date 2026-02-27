import asyncio
import os
import json
from rag_engine import rag_engine

async def verify():
    query = "ice cream price"
    print(f"Verifying metadata for query: {query}")
    
    result = await rag_engine.query(query)
    
    response_text = result.get("response", "")
    metadata = result.get("metadata", [])
    
    print("\n" + "="*50)
    print("RESPONSE TEXT PREVIEW:")
    print(response_text[:200] + "...")
    print("="*50)
    
    print(f"\nFound {len(metadata)} metadata items.")
    
    if metadata:
        first_item = metadata[0]
        print("\nFIRST METADATA ITEM KEYS:")
        print(list(first_item.keys()))
        
        print("\nMETADATA CONTENT (ALIASES CHECK):")
        for i, item in enumerate(metadata[:3]):
            print(f"\nItem {i}:")
            print(f"  Store: {item.get('store')}")
            print(f"  Product: {item.get('product')}")
            print(f"  Item Name (Size): {item.get('item_name')}")
            print(f"  Deal: {item.get('deal')}")
            print(f"  Image URL: {item.get('image_url')}")
            
        # Verify required keys for mobile
        required_keys = ['store', 'product', 'deal', 'image_url', 'item_name']
        missing = [k for k in required_keys if k not in first_item]
        if missing:
            print(f"\n❌ MISSING KEYS: {missing}")
        else:
            print("\n✅ ALL MOBILE-REQUIRED KEYS PRESENT!")

if __name__ == "__main__":
    asyncio.run(verify())
