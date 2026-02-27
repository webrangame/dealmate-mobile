import asyncio
import os
import json
from rag_engine import rag_engine

async def inspect():
    query = "ice cream price"
    print(f"Inspecting internal RAG nodes for: {query}")
    
    # We'll use the internal index to retrieve nodes
    retriever = rag_engine.index.as_retriever(similarity_top_k=5)
    nodes = retriever.retrieve(query)
    
    for i, node in enumerate(nodes):
        print(f"\n--- Node {i+1} (Score: {node.score:.4f}) ---")
        print(f"Text: {node.node.text[:100]}...")
        print(f"Metadata: {json.dumps(node.node.metadata, indent=2)}")

if __name__ == "__main__":
    asyncio.run(inspect())
