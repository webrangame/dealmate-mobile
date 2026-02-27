import asyncio
import json
import time
from rag_engine import rag_engine

# Curated list of 50 varied questions based on common supermarket items and data observed in the extraction
QUESTIONS = [
    "What is the price of Coles Australian Baby Beetroot 250g?",
    "How much are the Coles Classic Burgers?",
    "What is the price for Coles Simply Hamburger rolls 6 pack?",
    "Are there any deals on Tassal Smoked Salmon?",
    "Show me the price for Coles Tasmanian Fresh Salmon Skin On.",
    "What is the cost of Rana Filled Pasta 325g?",
    "Price for Berocca Immune Daily Defence Effervescent Tablets?",
    "How much is the Berocca Vitamin B & C Energy pk 45?",
    "What is the price of Ostelin Vitamin D3 1000IU Capsules Pk 250?",
    "Price for Ostelin Calcium & Vitamin D3 + K2 Tablets Pk 60?",
    "How much does Cenovis Sugarless C Chewable Tablets cost?",
    "What is the price for Nature's Own Glucosamine Sulfate?",
    "Are there discounts on Glad Aromatics kitchen tidy bags?",
    "How much is the Remedy Kombucha 750ml?",
    "What is the price of Daily Juice orange juice 2 litre?",
    "How much are the Optus X-Phones?",
    "What is the price of Listerine Freshburst antibacterial mouthwash 500ml?",
    "Price for Palmolive foam hand wash ref?",
    "How much are the Dove products on sale?",
    "What is the price for Finish ultimate dishwashing?",
    "Current price for Pringles Potato Crisps?",
    "How much are Zooper Dooper Water Ice?",
    "What is the price of Nature's Way kids smart probiotic?",
    "How much is the Swisse ultiboost magnesium glycinate?",
    "Price for Nature's Way vitamin c 50?",
    "What is the cost of Coles Australian Beef Mince?",
    "How much is a whole roast chicken?",
    "Price for Cadbury Dairy Milk chocolate block 180g?",
    "What is the price of Coca-Cola 30 pack?",
    "How much are the Huggies Nappies jumbo pk?",
    "What is the price for Kleenex Toilet Tissue 12 pack?",
    "Price of Sorbent Toilet Paper 10 pack?",
    "How much is the Omo Laundry Liquid 2L?",
    "What is the cost of Fairy Dishwasher Tablets 40pk?",
    "Price for Nescafe Blend 43 500g?",
    "How much is the Moccona Freeze Dried Coffee 400g?",
    "What is the price for Vegemite 560g?",
    "Price of Bega Peanut Butter 475g?",
    "How much is the Western Star Butter 500g?",
    "What is the price for Devondale Milk 2L?",
    "Price of A2 Milk 2L?",
    "How much are the Red Bull 4x250ml?",
    "What is the cost of V Energy Drink 4 pack?",
    "Price for Smiths Potato Chips 170g?",
    "How much are the Doritos 170g?",
    "What is the price of Kellogg's Corn Flakes 725g?",
    "Price of Sanitarium Weet-Bix 1.2kg?",
    "How much is the Uncle Tobys Oats 1kg?",
    "What is the price for Gippsland Yogurt 720g?",
    "Find the cheapest price for dishwashing liquid."
]

async def run_benchmark():
    results = []
    print(f"Starting Benchmark of {len(QUESTIONS)} questions...")
    print("=" * 50)
    
    start_total = time.time()
    
    for i, q in enumerate(QUESTIONS):
        print(f"[{i+1}/50] Testing: {q}")
        start_q = time.time()
        try:
            response = await rag_engine.query(q)
            duration = time.time() - start_q
            results.append({
                "question": q,
                "response": response,
                "duration": round(duration, 2),
                "success": "Product not found" not in response and "I am sorry" not in response
            })
            print(f"   Done in {duration:.2f}s | Success: {results[-1]['success']}")
        except Exception as e:
            print(f"   FAILED: {e}")
            results.append({"question": q, "error": str(e), "success": False})
            
    end_total = time.time()
    
    # Summary Statistics
    successful_finds = sum(1 for r in results if r.get("success"))
    total_time = end_total - start_total
    avg_time = total_time / len(QUESTIONS)
    
    summary = {
        "total_questions": len(QUESTIONS),
        "successful_finds": successful_finds,
        "failed_finds": len(QUESTIONS) - successful_finds,
        "total_duration_seconds": round(total_time, 2),
        "average_response_time": round(avg_time, 2)
    }
    
    print("\n" + "=" * 50)
    print("BENCHMARK SUMMARY")
    print("=" * 50)
    print(json.dumps(summary, indent=4))
    
    with open("benchmark_results.json", "w") as f:
        json.dump({"summary": summary, "details": results}, f, indent=4)
    print("\nFull results saved to benchmark_results.json")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
