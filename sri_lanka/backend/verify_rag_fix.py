import asyncio
import os
from rag_engine import rag_engine

async def test_queries():
    queries = [
        "Cat food specials",
        "ice cream price"
    ]
    
    for q in queries:
        print(f"\nQUERY: {q}")
        print("-" * 20)
        try:
            response = await rag_engine.query(q, user_id="test_verify")
            print(f"RESPONSE:\n{response}")
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_queries())
