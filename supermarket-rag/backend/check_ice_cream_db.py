import asyncio
import json
from rag_engine import RAGEngine

async def check_db_content():
    engine = RAGEngine()
    # We'll use the same keyword logic as the engine
    search_term = "ice cream"
    print(f"Searching DB for: {search_term}")
    
    nodes = engine._get_all_nodes(intent={"products": [search_term], "brands": ["Connoisseur"]})
    print(f"Found {len(nodes)} nodes.")
    
    for n in nodes:
        print(f"\n--- NODE ID: {n.node_id} ---")
        print(f"Metadata: {json.dumps(n.metadata, indent=2)}")
        print(f"Full Text:\n{n.text}")
        if "SAVE" in n.text:
             import re
             save_matches = re.finditer(r"SAVE\s*(\$?\d*\.?\d*)", n.text, re.I)
             for sm in save_matches:
                  print(f"Found SAVE phrase: '{sm.group(0)}' (Amount: '{sm.group(1)}')")

if __name__ == "__main__":
    asyncio.run(check_db_content())
