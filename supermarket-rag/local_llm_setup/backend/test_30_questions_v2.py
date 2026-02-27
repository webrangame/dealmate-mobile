import httpx
import asyncio
import json
import time

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"
USER_ID = "bulk_tester_30_v2"

QUESTIONS = [
    "What is the price of Dine Wet Cat Food Pk 7 x 85g?",
    "How much is Purina One Dry Cat Food 1.4-1.5 kg?",
    "Is Fancy Feast Classics Wet Cat Food 85g on sale?",
    "Price of Temptations Cat Treats 85g?",
    "What is the current deal for Supercoat Dry Dog Food 2.6-2.8 kg?",
    "How much is Breeder's Choice Cat Litter 24 Litre?",
    "Price of Pedigree Dry Dog Food 8 kg?",
    "What is the price of Radiant Laundry Capsules in Coles?",
    "Do you have Canadian Club in Coles? List the price.",
    "Price of Coles RSPCA Approved Chicken Schnitzel 600g?",
    "How much is Kelloggs LCMs 100g-138g?",
    "Price of Berocca Immune Effervescent Tablets 15 Pack?",
    "Is there a deal for Nivea Body Wash 1 Litre?",
    "Price of Colgate Advanced Whitening Toothpaste 115g?",
    "How much is Garnier Fructis Shampoo 315mL?",
    "Price of Herbal Essences Classics Shampoo 400mL?",
    "What is the deal for Peters Drumstick 4 Pack - 6 Pack?",
    "Price of Smith's Potato Chips 170g?",
    "How much is Pepsi Max 10x375ml?",
    "Price of Fairy Original Dishwasher Tablets 22 Pack?",
    "Is Morning Fresh Dishwashing Liquid 400mL on sale?",
    "Price of Carefree Barely There Liners 42 Pack?",
    "How much is Ogx Extra Strength Shampoo 385mL?",
    "Garnier Vitamin C Micellar Water 400mL price?",
    "Price of Buller Cream 200mL?",
    "What is the price of Delectables Lickable Stew Cat Treats 40g?",
    "How much is Pretty Wild Soup Cat Treats 155g?",
    "Price of Churu Puree Cat Treats Pk 4?",
    "Is My Dog Wet Dog Food Pk 6 x 100g on sale?",
    "Price of Schmackos Strapz Dog Treats 500g?"
]

async def test_query(client, q):
    start = time.time()
    payload = {"text": q, "user_id": USER_ID}
    try:
        resp = await client.post(API_URL, json=payload, timeout=60.0)
        duration = time.time() - start
        if resp.status_code == 200:
            result = resp.json()["response"]
            # A success is if it doesn't give the 'confidence' apology AND it finds a price or store
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
        # Run in smaller batches to avoid overwhelming the service
        batch_size = 5
        results = []
        for i in range(0, len(QUESTIONS), batch_size):
            batch = QUESTIONS[i:i+batch_size]
            print(f"Testing batch {i//batch_size + 1}/{(len(QUESTIONS)-1)//batch_size + 1}...")
            tasks = [test_query(client, q) for q in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            time.sleep(2) # Brief pause between batches
    
    with open("test_results_30_v2.json", "w") as f:
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
