
import httpx
import json
import asyncio
import time

API_URL = "http://localhost:8000/chat"

DUAL_PRODUCTS = [
    "milk", "bread", "butter", "eggs", "apples", 
    "bananas", "yogurt", "pasta", "soft drink", "coffee"
]

async def run_dual_test(query, client):
    try:
        response = await client.post(API_URL, json={"text": query, "user_id": "dual_tester"}, timeout=60.0)
        data = response.json()
        
        # Check shops in response
        resp_text = data.get("response", "").lower()
        has_coles = "coles" in resp_text
        has_woolworths = "woolworths" in resp_text
        
        # Check images
        metadatas = data.get("metadata", [])
        image_urls = [m.get("image_url", "") for m in metadatas]
        specific_ones = [url for url in image_urls if "_item" in (url or "")]
        
        return {
            "query": query,
            "both_shops": has_coles and has_woolworths,
            "coles_found": has_coles,
            "wool_found": has_woolworths,
            "total_images": len(image_urls),
            "specific_crops": len(specific_ones),
            "status": response.status_code
        }
    except Exception as e:
        return {"query": query, "error": str(e)}

async def main():
    print("=== Supermarket RAG Dual-Shop Test (10 Products) ===")
    results = []
    async with httpx.AsyncClient() as client:
        for product in DUAL_PRODUCTS:
            res = await run_dual_test(product, client)
            results.append(res)
            
            both_str = "✅ YES" if res.get("both_shops") else "❌ NO"
            print(f"Product: '{product:10}' | Both Shops: {both_str} | Images: {res.get('total_images')} | Specific: {res.get('specific_crops')}")

    print("\nSummary:")
    both_count = sum(1 for r in results if r.get("both_shops"))
    print(f"- Total Products: {len(DUAL_PRODUCTS)}")
    print(f"- Products found in both shops: {both_count}")
    
    with open("dual_shop_test_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
