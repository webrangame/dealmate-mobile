import httpx
import asyncio
import json
import time

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"
USER_ID = "bulk_tester_30"

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
            success = "confiden" not in result.lower() and "not found" not in result.lower()
            return {"question": q, "success": success, "response": result, "duration": duration}
        else:
            return {"question": q, "success": False, "error": f"HTTP {resp.status_code}", "duration": duration}
    except Exception as e:
        return {"question": q, "success": False, "error": str(e), "duration": time.time() - start}

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [test_query(client, q) for q in QUESTIONS]
        results = await asyncio.gather(*tasks)
    
    with open("test_results_30.json", "w") as f:
        json.dump(results, f, indent=2)
    
    total = len(results)
    successes = sum(1 for r in results if r["success"])
    print(f"Test Complete: {successes}/{total} successful.")
    
    for r in results:
        status = "PASS" if r["success"] else "FAIL"
        print(f"[{status}] {r['question']}")
        if not r["success"]:
            print(f"      Reason: {r.get('error') or 'Confidence issue or Not found'}")

if __name__ == "__main__":
    asyncio.run(main())
