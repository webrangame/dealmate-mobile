import asyncio
import json
import os
import sys
from dotenv import load_dotenv
from rag_engine import RAGEngine

# Redirect stdout to capture logs
import io
log_capture = io.StringIO()
old_stdout = sys.stdout
sys.stdout = log_capture

async def main():
    # Load environment variables
    load_dotenv()
    
    engine = RAGEngine()
    
    query_text = "is there rice"
    user_id = "manual_search_rice_debug"
    
    result = await engine.query(query_text, user_id=user_id)
    
    # Restore stdout
    sys.stdout = old_stdout
    logs = log_capture.getvalue()
    
    print("LOGS:")
    print(logs)
    
    print("\n" + "="*50)
    print("SEARCH RESULT")
    print("="*50)
    print(result.get("response", "No response found."))
    print("\n" + "="*50)
    print("METADATA (Images found)")
    print("="*50)
    metadata = result.get("metadata", [])
    if metadata:
        for i, m in enumerate(metadata):
            print(f"{i+1}. Store: {m.get('shop_name')}, Product: {m.get('product_name')}, Price: {m.get('price')}")
            # print(f"   Image: {m.get('image_url')}")
    else:
        print("No images found in metadata.")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
