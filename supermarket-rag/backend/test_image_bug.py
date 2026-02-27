import asyncio
import json
import os
from rag_engine import RAGEngine

async def test_ice_cream_images():
    engine = RAGEngine()
    query_text = "i need to eat ice cream today"
    user_id = "test_image_user"
    
    # We will hook into the internals by just running the query and then
    # printing out the metadata list explicitly
    # To do this without modifying rag_engine.py too much, we just rely on its output.
    # Actually, I'll modify the script to print the raw response metadata
    result = await engine.query(query_text, user_id=user_id)
    
    print("\n--- Response Text ---")
    print(result.get("response", ""))
    
    print("\n--- Metadata Images Returned ---")
    metadata = result.get("metadata", [])
    print(f"Total images: {len(metadata)}")
    
    for i, meta in enumerate(metadata):
        print(f"[{i+1}] {meta.get('product_name', 'Unknown')} - {meta.get('shop', 'Unknown')} - {meta.get('image_url')}")

if __name__ == "__main__":
    asyncio.run(test_ice_cream_images())
