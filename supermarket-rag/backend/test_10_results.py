import asyncio
import httpx
import json
import time

API_URL = "http://localhost:8000/chat"
USER_ID = "test_user_10_local"

QUESTIONS = [
    "What is the price of eggs?",
    "How much for Tim Tams?",
    "SunRice rice price",
    "Best milk at Coles",
    "Woolworths bread price",
    "Coca Cola 24 pack deal",
    "Cadbury dairy milk price",
    "Devondale butter cost",
    "Finish dishwasher tabs deals",
    "Nescafe blend 43 500g price"
]

async def test_question(client, question, q_id):
    print(f"[{q_id}/10] Testing: {question}")
    start = time.time()
    try:
        resp = await client.post(API_URL, json={"text": question, "user_id": USER_ID}, timeout=90.0)
        dur = time.time() - start
        if resp.status_code == 200:
            return {"id": q_id, "question": question, "status": "SUCCESS", "duration": round(dur, 2)}
        else:
            return {"id": q_id, "question": question, "status": f"ERROR {resp.status_code}", "duration": round(dur, 2)}
    except Exception as e:
        return {"id": q_id, "question": question, "status": "EXCEPTION", "error": str(e), "duration": round(time.time() - start, 2)}

async def run():
    print(f"Starting Final 10-Question Test against {API_URL}")
    results = []
    async with httpx.AsyncClient() as client:
        for i, q in enumerate(QUESTIONS):
            results.append(await test_question(client, q, i+1))
            
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    print(f"\nSummary: {success_count}/10 successful")
    
    with open("test_results_local_10.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    asyncio.run(run())
