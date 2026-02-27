import asyncio
import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "supermarket-rag", "backend"))

from rag_engine import RAGEngine

async def test_live_query():
    load_dotenv(os.path.join("supermarket-rag", "backend", ".env"))
    
    engine = RAGEngine()
    
    # Query for the specifically problematic product
    query_text = "how much is connoisseur ice cream 1L at woolworths?"
    print(f"\n--- Testing Query: '{query_text}' ---\n")
    
    response = await engine.query(query_text, user_id="test_user@example.com")
    
    print("\n--- FINAL RESPONSE ---\n")
    print(response.get("response"))
    print("\n--- METADATA ---\n")
    for m in response.get("metadata", []):
        print(f"- {m.get('product')}: {m.get('price')} ({m.get('store')}) {'[LIVE]' if m.get('is_live') else '[CATALOG]'}")

if __name__ == "__main__":
    asyncio.run(test_live_query())
