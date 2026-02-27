import asyncio
import json
import os
import sys
from dotenv import load_dotenv
from rag_engine import RAGEngine

# Patch RAGEngine.query to print fetched nodes
original_query = RAGEngine.query

async def patched_query(self, text, user_id=None):
    # This is a bit tricky to patch because it's an async method
    # and we want to see variables inside it.
    # Instead, let's just use the logs and modify the engine temporarily if needed.
    return await original_query(self, text, user_id)

async def main():
    load_dotenv()
    
    engine = RAGEngine()
    
    # We will manually duplicate some logic from query() to see what's happening
    print("DEBUG: Fetching nodes manually for 'is there rice'...")
    intent = {"product": "rice", "brand": None, "shop": None, "category": "Pantry", "excluded_terms": ["cracker", "cake", "crispy", "flour"]}
    nodes = engine._get_all_nodes(intent=intent)
    print(f"DEBUG: Manually fetched {len(nodes)} nodes.")
    for i, n in enumerate(nodes[:10]):
        print(f"Node {i}:")
        print(f"  Metadata: {n.metadata}")
        print(f"  Text: {n.text[:200]}...")
    
    print("\n" + "="*50)
    print("RUNNING FULL QUERY")
    print("="*50)
    result = await engine.query("is there rice", user_id="manual_search_debug_2")
    print(result.get("response"))

if __name__ == "__main__":
    asyncio.run(main())
