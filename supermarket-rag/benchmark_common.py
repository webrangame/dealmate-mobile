import asyncio
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

async def run_common_benchmark():
    # Items known to be in both or similar
    common_items = [
        "Pringles",
        "Coca Cola 30 pack", 
        "Mount Franklin Water",
        "Dairy Farmers Yoghurt", 
        "Cadbury Favourites"
    ]
    
    output_file = "benchmark_common_results.md"
    
    with open(output_file, "w") as f:
        f.write("# RAG Benchmark: Common Product Comparisons\n\n")
    
    for name in common_items:
        query = f"Compare prices for {name}"
        print(f"Querying: {name}...")
        
        try:
            response = await rag_engine.query(query)
            
            with open(output_file, "a") as f:
                f.write(f"## Query: {name}\n")
                f.write(f"**RAG Response:**\n\n")
                f.write(f"{response}\n\n")
                f.write("---\n\n")
                
        except Exception as e:
            print(f"Error querying {name}: {e}")

    print(f"\nCommon benchmark complete. Results saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(run_common_benchmark())
