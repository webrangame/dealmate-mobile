import asyncio
import json
import time
import os
from rag_engine import RAGEngine

async def run_test():
    engine = RAGEngine()
    user_id = "itranga@gmail.com"
    
    # Verify key first
    key = await engine._ensure_user_key(user_id)
    print(f"Using user_id: {user_id}")
    print(f"Resolved Key: {key[:7]}...{key[-4:]}")
    
    general_queries = [
        "where is sri lanka?",
        "what is the capital of France?",
        "who are you?",
        "how can I use this app?",
        "tell me a joke",
        "what's the weather like?",
        "give me some healthy eating tips",
        "how to save money on grocery shopping?",
        "who is the prime minister of Australia?",
        "what time is it?",
        "hello there",
        "good morning",
        "what is 2+2?",
        "how do I find cheap items?",
        "is it going to rain today?",
        "what is the tallest mountain in the world?",
        "who founded Apple?",
        "how many legs does a spider have?",
        "what is the largest ocean?",
        "thank you"
    ]
    
    product_queries = [
        "price of Berocca",
        "how much is milk?",
        "Coles bread price",
        "Woolworths eggs cost",
        "cheapest coffee",
        "Cadbury chocolate deals",
        "Coke 24 pack price",
        "Finish ultimate plus price",
        "Huggies nappies deals",
        "Sukin skincare price",
        "A2 milk price",
        "Omo laundry liquid cost",
        "Milo 1kg price",
        "Vegemite 380g cost",
        "Peters ice cream price",
        "Red Bull 4 pack",
        "Head & Shoulders shampoo",
        "Oral-B toothpaste",
        "Whiskas cat food",
        "Pedigree dog food"
    ]
    
    results = {
        "user_id": user_id,
        "key_used": f"{key[:7]}...",
        "general": [],
        "product": []
    }
    
    print("\n--- Testing General Queries ---")
    for i, q in enumerate(general_queries):
        start = time.time()
        print(f"[{i+1}/20] Query: {q}", end=" ", flush=True)
        try:
            response = await engine.query(q, user_id=user_id)
            elapsed = time.time() - start
            results["general"].append({
                "query": q, 
                "response": response,
                "time": f"{elapsed:.2f}s"
            })
            print(f"(OK - {elapsed:.2f}s)")
        except Exception as e:
            print(f"(FAILED: {e})")
            results["general"].append({"query": q, "response": f"ERROR: {e}"})

    print("\n--- Testing Product Queries ---")
    for i, q in enumerate(product_queries):
        start = time.time()
        print(f"[{i+1}/20] Query: {q}", end=" ", flush=True)
        try:
            response = await engine.query(q, user_id=user_id)
            elapsed = time.time() - start
            results["product"].append({
                "query": q, 
                "response": response,
                "time": f"{elapsed:.2f}s"
            })
            print(f"(OK - {elapsed:.2f}s)")
        except Exception as e:
            print(f"(FAILED: {e})")
            results["product"].append({"query": q, "response": f"ERROR: {e}"})
        
    with open("benchmark_results_itranga_final.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Generate a summary markdown
    with open("benchmark_results_itranga_summary.md", "w") as f:
        f.write(f"# Benchmark Results for {user_id}\n\n")
        f.write(f"**Key Used**: `{key[:7]}...{key[-4:]}`\n\n")
        
        f.write("## General Queries\n")
        f.write("| # | Query | Response Sample | Time |\n")
        f.write("|---|-------|-----------------|------|\n")
        for i, r in enumerate(results["general"]):
            resp = str(r['response']).replace('\n', ' ')[:50] + "..."
            f.write(f"| {i+1} | {r['query']} | {resp} | {r['time']} |\n")
            
        f.write("\n## Product Queries\n")
        f.write("| # | Query | Response Sample | Time |\n")
        f.write("|---|-------|-----------------|------|\n")
        for i, r in enumerate(results["product"]):
            resp = str(r['response']).replace('\n', ' ')[:50] + "..."
            f.write(f"| {i+1} | {r['query']} | {resp} | {r['time']} |\n")

    print(f"\nBenchmark complete! Results saved to benchmark_results_itranga_final.json and summary.md")

if __name__ == "__main__":
    asyncio.run(run_test())
