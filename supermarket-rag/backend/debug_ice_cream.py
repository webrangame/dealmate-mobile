import asyncio
import json
from rag_engine import RAGEngine

async def debug_query():
    engine = RAGEngine()
    query_text = "ice cream price"
    print(f"Executing debug query: {query_text}")
    
    # We'll use a mocked user_id to simulate previous history if any, but start fresh
    user_id = "debug_user"
    
    # Run the query (non-streaming for simplicity in output capture)
    result = await engine.query(query_text, user_id=user_id, stream=False)
    
    print("\n--- LLM RESPONSE ---\n")
    print(result.get("response"))
    
    print("\n--- METADATA ---\n")
    print(json.dumps(result.get("metadata", []), indent=2))

if __name__ == "__main__":
    asyncio.run(debug_query())
