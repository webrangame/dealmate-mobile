import asyncio
import httpx
import json
import time
import os

API_URL = "http://localhost:8000/chat"
USER_ID = "test_user_20_local"

QUESTIONS = [
    "Price of milk", "How much is Coca Cola?", "Cheapest bread", "Cost of bananas", "Price of eggs",
    "Woolworths pasta sauce", "Cadbury chocolate", "Price of Tim Tams", "Frozen chips price", "Toilet paper price",
    "Nescafe coffee price", "Best deal on rice", "Price of chicken breast", "Coles ice cream", "Olive oil cost",
    "Detergent price", "Shampoo deals", "Dog food price", "Cat food specials", "Price of butter"
]

async def test_question(client, question, q_id):
    print(f"[{q_id}/20] Testing: {question}")
    start = time.time()
    try:
        resp = await client.post(API_URL, json={"text": question, "user_id": USER_ID}, timeout=90.0)
        dur = time.time() - start
        if resp.status_code == 200:
            data = resp.json()
            # Basic heuristic for "success": found mention of shops in response
            shops_found = []
            if "coles" in data["response"].lower(): shops_found.append("Coles")
            if "woolworths" in data["response"].lower(): shops_found.append("Woolworths")
            
            return {
                "id": q_id, "question": question, "status": "SUCCESS", 
                "duration": round(dur, 2), "shops": shops_found,
                "has_metadata": len(data.get("metadata", [])) > 0
            }
        else:
            return {"id": q_id, "question": question, "status": f"ERROR {resp.status_code}", "error": resp.text, "duration": round(time.time() - start, 2)}
    except Exception as e:
        return {"id": q_id, "question": question, "status": "EXCEPTION", "error": str(e), "duration": round(time.time() - start, 2)}

async def run():
    print(f"Starting Local 20-Question Test against {API_URL}")
    results = []
    async with httpx.AsyncClient() as client:
        for i, q in enumerate(QUESTIONS):
            results.append(await test_question(client, q, i+1))
            
    with open("test_results_local_20.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n=== TEST SUMMARY ===")
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    multi_shop_count = sum(1 for r in results if r.get("shops") and len(r["shops"]) > 1)
    
    print(f"Total Questions: {len(QUESTIONS)}")
    print(f"Success: {success_count}")
    print(f"Multi-Shop Results: {multi_shop_count}")
    print("Full results saved to test_results_local_20.json")

if __name__ == "__main__":
    asyncio.run(run())
