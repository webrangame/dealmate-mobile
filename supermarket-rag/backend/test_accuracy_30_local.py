import asyncio
import httpx
import json
import os
import time

# Configuration
API_URL = "http://localhost:8002/chat"
USER_ID = "accuracy_tester_30"

QUESTIONS = [
    "What is the price of Arnott's Shapes at Coles?",
    "How much is Devondale Milk Powder at Woolworths?",
    "Show me deals for Coca-Cola 30 pack.",
    "Best price for Ice Cream at Coles?",
    "Price of Pak Choy at Coles?",
    "Is there any discount on Cadbury Dairy Milk at Woolworths?",
    "Cost of Australian Premium Strawberries at Coles?",
    "How much for Annalisa Tomatoes at Woolworths?",
    "Price of Tim Tam at Coles?",
    "Deals on laundry detergent at Woolworths?",
    "Price of Bread at Coles?",
    "How much is Butter at Woolworths?",
    "Price of Eggs 12 pack at Coles?",
    "Deals on Chicken Breast at Woolworths?",
    "Price of Bananas at Coles?",
    "How much is Toilet Paper at Woolworths?",
    "Price of Pavlova base at Coles?",
    "Deals on Coffee pods at Woolworths?",
    "Price of Olive Oil 1L at Coles?",
    "How much is Rice 5kg at Woolworths?",
    "What is the price of Dine Wet Cat Food Pk 7 x 85g?",
    "How much is Purina One Dry Cat Food 1.4-1.5 kg?",
    "Is Fancy Feast Classics Wet Cat Food 85g on sale?",
    "Price of Temptations Cat Treats 85g?",
    "What is the current deal for Supercoat Dry Dog Food 2.6-2.8 kg?",
    "How much is Breeder's Choice Cat Litter 24 Litre?",
    "Price of Pedigree Dry Dog Food 8 kg?",
    "Is Morning Fresh Dishwashing Liquid 400mL on sale?",
    "Price of Smith's Potato Chips 170g?",
    "How much is Pepsi Max 10x375ml?"
]

async def test_query(client, q):
    start = time.time()
    payload = {"text": q, "user_id": USER_ID}
    try:
        resp = await client.post(API_URL, json=payload, timeout=60.0)
        duration = time.time() - start
        if resp.status_code == 200:
            data = resp.json()
            response_text = data.get("response", "")
            metadata = data.get("metadata", [])
            
            # Check if we have a results table in the response
            has_table = "|---|---|---|---|" in response_text or "| Product | Store | Price |" in response_text
            
            # Check if it's a "Product not found" message
            # Template rule 6: 'say Product not found'
            is_explicit_not_found = "product not found" in response_text.lower() and not has_table
            
            # Final result: success if we have a table OR if it's a polite helpful answer
            # many successful answers might still say "Product not found at Woolworths" if only one shop has it.
            has_answer = (has_table or len(response_text) > 50) and not is_explicit_not_found
            
            # Check for images in metadata
            has_images = any(m.get("image_url") for m in metadata)
            
            # Final result
            success = has_answer and has_images
            
            return {
                "question": q,
                "success": success,
                "has_answer": has_answer,
                "has_images": has_images,
                "num_images": len(metadata),
                "duration": duration,
                "response": response_text[:200] + "..." if len(response_text) > 200 else response_text
            }
        else:
            return {"question": q, "success": False, "error": f"HTTP {resp.status_code}", "duration": duration}
    except Exception as e:
        return {"question": q, "success": False, "error": str(e), "duration": time.time() - start}

async def main():
    print(f"Starting Accuracy Test for 30 Product Questions on {API_URL}...")
    async with httpx.AsyncClient() as client:
        # Run sequentially to avoid overwhelming LiteLLM or getting rate limited by Gemini
        results = []
        for i, q in enumerate(QUESTIONS):
            print(f"[{i+1}/30] Testing: {q}", end=" ", flush=True)
            res = await test_query(client, q)
            results.append(res)
            if res.get("success"):
                print("-> PASS")
            else:
                reason = res.get("error") or (f"Ans:{res.get('has_answer')} Img:{res.get('has_images')}")
                print(f"-> FAIL ({reason})")
            await asyncio.sleep(1) # Politeness delay
    
    with open("accuracy_test_results_30.json", "w") as f:
        json.dump(results, f, indent=2)
    
    total = len(results)
    successes = sum(1 for r in results if r.get("success"))
    ans_count = sum(1 for r in results if r.get("has_answer"))
    img_count = sum(1 for r in results if r.get("has_images"))
    
    print("\n" + "="*40)
    print(f"ACCURACY REPORT")
    print(f"Total Questions: {total}")
    print(f"Proper Answers: {ans_count}/{total}")
    print(f"Images Found:   {img_count}/{total}")
    print(f"Full Success:   {successes}/{total}")
    print("="*40)
    
    # Generate Markdown Summary
    summary = f"# RAG Accuracy Report (30 Products)\n\n"
    summary += f"- **Success Rate**: {successes}/{total} ({successes/total*100:.1f}%)\n"
    summary += f"- **Answer Rate**: {ans_count}/{total} ({ans_count/total*100:.1f}%)\n"
    summary += f"- **Image metadata Rate**: {img_count}/{total} ({img_count/total*100:.1f}%)\n\n"
    summary += "| Status | Question | Answer | Images |\n"
    summary += "|---|---|---|---|\n"
    for r in results:
        status = "✅" if r.get("success") else "❌"
        ans = "Yes" if r.get("has_answer") else "No"
        imgs = f"{r.get('num_images', 0)}" if r.get("has_images") else "0"
        summary += f"| {status} | {r['question']} | {ans} | {imgs} |\n"
    
    with open("accuracy_report_30.md", "w") as f:
        f.write(summary)
    
    print("\nDetailed report saved to accuracy_report_30.md")

if __name__ == "__main__":
    asyncio.run(main())
