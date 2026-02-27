import asyncio
import os
from rag_engine import RAGEngine

async def verify_fix():
    print("Initializing RAG Engine...")
    engine = RAGEngine()
    
    query = "ice cream price"
    print(f"\nQuerying: '{query}'")
    
    # We'll use a modified version of the query method logic to inspect internal state
    # or just call it and trust the output for now, but let's add some print debugging to rag_engine.py temporarily
    
    result = await engine.query(query)
    response_text = result.get("response", "")
    metadata = result.get("metadata", [])
    
    print("\n=== RESPONSE ===")
    print(response_text)
    
    # Check what shops were actually retrieved in the response metadata
    retrieved_shops = set([m.get("shop_name") for m in metadata])
    print(f"\nShops in metadata: {retrieved_shops}")
    
    print("\n=== METADATA (IMAGES) ===")
    for m in metadata:
        print(f"- {m.get('shop_name')} (Page {m.get('page')}): {m.get('image_url')}")
    
    # Verification checks
    coles_present = "Coles" in response_text
    woolworths_present = "Woolworths" in response_text
    
    print("\n=== VERIFICATION ===")
    print(f"Coles found: {coles_present}")
    print(f"Woolworths found: {woolworths_present}")
    
    if coles_present and woolworths_present:
        print("✅ SUCCESS: Both shops are present in the response.")
    else:
        if not coles_present:
            print("❌ FAILURE: Coles missing from response.")
        if not woolworths_present:
            print("❌ FAILURE: Woolworths missing from response.")

if __name__ == "__main__":
    asyncio.run(verify_fix())
