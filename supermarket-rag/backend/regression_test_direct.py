import asyncio
import json
import time
import os
from dotenv import load_dotenv
from rag_engine import RAGEngine

QUESTIONS = [
    "Price of milk", "How much is Coca Cola?", "Cheapest bread", "Cost of bananas", "Price of eggs",
    "Woolworths pasta sauce", "Cadbury chocolate", "Price of Tim Tams", "Frozen chips price", "Toilet paper price",
    "Nescafe coffee price", "Best deal on rice", "Price of chicken breast", "Coles ice cream", "Olive oil cost",
    "Detergent price", "Shampoo deals", "Dog food price", "Cat food specials", "Price of butter"
]

async def test_question(engine, question, q_id):
    print(f"[{q_id}/{len(QUESTIONS)}] Testing: {question}")
    start = time.time()
    try:
        data = await engine.query(question, user_id="regression_test")
        dur = time.time() - start
        
        response_text = data.get("response", "").lower()
        shops_found = []
        if "coles" in response_text: shops_found.append("Coles")
        if "woolworths" in response_text: shops_found.append("Woolworths")
        
        metadata = data.get("metadata", [])
        return {
            "id": q_id, "question": question, "status": "SUCCESS", 
            "duration": round(dur, 2), "shops": shops_found,
            "has_metadata": len(metadata) > 0,
            "metadata_count": len(metadata)
        }
    except Exception as e:
        return {"id": q_id, "question": question, "status": "EXCEPTION", "error": str(e), "duration": round(time.time() - start, 2)}

async def run():
    load_dotenv()
    print("Initialising RAGEngine for regression testing...")
    engine = RAGEngine()
    
    results = []
    for i, q in enumerate(QUESTIONS):
        results.append(await test_question(engine, q, i+1))
            
    with open("regression_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n=== REGRESSION TEST SUMMARY ===")
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    metadata_count = sum(1 for r in results if r.get("has_metadata"))
    
    print(f"Total Questions: {len(QUESTIONS)}")
    print(f"Success (LLM Answered): {success_count}")
    print(f"With Metadata (Products Found): {metadata_count}")
    
    for r in results:
        if not r.get("has_metadata") and r["status"] == "SUCCESS":
            print(f"  [!] No metadata for: {r['question']}")

    print("\nFull results saved to regression_test_results.json")

if __name__ == "__main__":
    asyncio.run(run())
