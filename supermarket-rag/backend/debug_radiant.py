import asyncio
import os
from rag_engine import RAGEngine

async def test_radiant_query():
    # Load env vars for RAG
    # Settings should be already configured in rag_engine.py __init__
    
    re = RAGEngine()
    query_text = "What is the price of Radiant Laundry Capsules?"
    user_id = "debug_user"
    
    print(f"--- Running Query: {query_text} ---")
    response = await re.query(query_text, user_id)
    
    print("\n--- FINAL RESPONSE ---")
    print(response)

if __name__ == "__main__":
    asyncio.run(test_radiant_query())
