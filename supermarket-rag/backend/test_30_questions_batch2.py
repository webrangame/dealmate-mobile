import httpx
import asyncio
import json
import time

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"
USER_ID = "bulk_tester_30_batch2"

QUESTIONS = [
    "What is the price of Arnott's Scotch Finger 250g in Coles?",
    "How much is Arnott's Tina Wafer 250g?",
    "Is Arnott's Hundreds & Thousands on sale in Coles?",
    "Price of Iced Vovo Biscuits 200g-210g?",
    "What is the deal for Sukin Hand Wash 500ml in Coles?",
    "How much is Sunsilk Shampoo 700ml in Coles?",
    "Price of Vaseline Intensive Care Body Lotion 750ml?",
    "What is the price of John Frieda Premium Shampoo 250ml?",
    "How much is Revlon Illuminance Glow Filter 30ml in Coles?",
    "Price of U By Kotex Ultrathins Pk 8-16?",
    "Is Sensodyne Repair & Protect Toothpaste 100g on sale?",
    "Price of Essano Hydration+ Daily Facial Moisturiser 100ml?",
    "How much is the Metallic Heart Garland 180cm in Coles?",
    "Price of Bear With Heart and Patch in Coles?",
    "What is the price of Date Box in Coles?",
    "How much is Woolworths American Style Slaw Kit 450g?",
    "Price of Australian Corn Cobbettes 425g Pack in Woolworths?",
    "Is Woolworths BBQ Texas Style Butterflied Boneless Chicken on sale?",
    "How much are Woolworths Australian Beef Burgers 400-500g?",
    "Price of Australian Pork Shoulder Boneless Roast in Woolworths?",
    "What is the deal for Woolworths Marinated Kebab Varieties 750g Pk 12?",
    "Price of Macro Free Range Australian Fresh Whole Plain Chicken?",
    "How much is Australian Fresh RSPCA Approved Chicken Breast Diced 1kg?",
    "What is the price of Australian Beef Rump Steak Bulk Pack in Woolworths?",
    "Price of Thawed Large Australian Cooked Tiger Prawns?",
    "How much is Fresh Tasmanian Atlantic Salmon Fillets Skin On in Woolworths?",
    "Price of Woolworths Pasta Spirals 500g?",
    "How much is Barilla Pasta Risoni 500g in Woolworths?",
    "Is Australian Fresh RSPCA Approved Chicken Breast Fillets on sale?",
    "What is the price of Australian Lamb Leg Roast in Woolworths?"
]

async def test_query(client, q):
    start = time.time()
    payload = {"text": q, "user_id": USER_ID}
    try:
        resp = await client.post(API_URL, json=payload, timeout=60.0)
        duration = time.time() - start
        if resp.status_code == 200:
            result = resp.json()["response"]
            is_apology = "confidence" in result.lower() or "couldn't verify" in result.lower()
            not_found = "Product not found" in result
            success = not is_apology and not not_found
            
            status = "PASS"
            if is_apology: status = "CONFIDENCE_FAIL"
            elif not_found: status = "NOT_FOUND"
            
            return {"question": q, "status": status, "response": result, "duration": duration}
        else:
            return {"question": q, "status": "ERROR", "error": f"HTTP {resp.status_code}", "duration": duration}
    except Exception as e:
        return {"question": q, "status": "ERROR", "error": str(e), "duration": time.time() - start}

async def main():
    async with httpx.AsyncClient() as client:
        batch_size = 5
        results = []
        for i in range(0, len(QUESTIONS), batch_size):
            batch = QUESTIONS[i:i+batch_size]
            print(f"Testing batch {i//batch_size + 1}/{(len(QUESTIONS)-1)//batch_size + 1}...")
            tasks = [test_query(client, q) for q in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            time.sleep(2)
    
    with open("test_results_30_batch2.json", "w") as f:
        json.dump(results, f, indent=2)
    
    total = len(results)
    passes = sum(1 for r in results if r["status"] == "PASS")
    print(f"\n--- Final Results ({passes}/{total} PASS) ---")
    
    for r in results:
        print(f"[{r['status']}] {r['question']}")
        if r["status"] != "PASS":
            msg = r.get("error") or r["response"][:100] + "..."
            print(f"      {msg}")

if __name__ == "__main__":
    asyncio.run(main())
