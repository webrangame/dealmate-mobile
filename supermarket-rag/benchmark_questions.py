import asyncio
import json
import random
import os
import sys

# Ensure we can import from backend
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from rag_engine import rag_engine
except ImportError:
    # Fallback if running from a different directory
    sys.path.append(os.path.join(os.getcwd(), '../backend'))
    from rag_engine import rag_engine

async def run_benchmark():
    # 1. Load products
    json_path = 'product_listings_vision/all_products.json'
    if not os.path.exists(json_path):
        print("Error: Products JSON not found.")
        return

    with open(json_path, 'r') as f:
        products = json.load(f)

    # 2. Select 50 random products
    # We want a mix, but let's try to pick unique names to avoid duplicates in selection
    unique_names = list(set([p['name'] for p in products]))
    
    # If we have enough products, take 50, else take all
    sample_size = min(50, len(unique_names))
    selected_names = random.sample(unique_names, sample_size)
    
    print(f"Selected {sample_size} random products for benchmarking.")
    
    results = []
    
    # 3. Query RAG for each
    output_file = "benchmark_results_50.md"
    
    with open(output_file, "w") as f:
        f.write("# RAG Benchmark: 50 Random Product Comparisons\n\n")
        f.write(f"**Date:** {os.popen('date').read().strip()}\n\n")
        f.write("---\n\n")

    for i, name in enumerate(selected_names, 1):
        query = f"Compare prices for {name}"
        print(f"[{i}/{sample_size}] Querying: {name}...")
        
        try:
            response = await rag_engine.query(query)
            
            # Append to file immediately
            with open(output_file, "a") as f:
                f.write(f"## {i}. Query: {name}\n")
                f.write(f"**Prompt:** {query}\n\n")
                f.write(f"**RAG Response:**\n\n")
                f.write(f"{response}\n\n")
                f.write("---\n\n")
                
        except Exception as e:
            print(f"Error querying {name}: {e}")
            with open(output_file, "a") as f:
                f.write(f"## {i}. Query: {name}\n")
                f.write(f"**Error:** {str(e)}\n\n")
                f.write("---\n\n")

    print(f"\nBenchmark complete. Results saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
