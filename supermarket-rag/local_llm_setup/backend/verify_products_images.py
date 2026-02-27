import asyncio
import httpx
import json
import time

API_URL = "http://localhost:8000/chat"
USER_ID = "verify_products_images_user"

PRODUCTS = [
    "milk", "bread", "butter", "eggs", "cheese",
    "chicken", "beef", "rice", "pasta", "tomato",
    "potato", "onion", "carrot", "apple", "banana",
    "orange", "yogurt", "chocolate", "coffee", "tea"
]

async def verify_product(client, product, index):
    query = f"{product} price"
    start_time = time.time()
    
    try:
        response = await client.post(
            API_URL, 
            json={"text": query, "user_id": USER_ID}, 
            timeout=60.0
        )
        duration = time.time() - start_time
        
        if response.status_code != 200:
            return {
                "product": product,
                "status": f"ERROR {response.status_code}",
                "coles": "N/A",
                "woolworths": "N/A",
                "images": 0,
                "image_match": "N/A",
                "duration": duration,
                "raw_images": []
            }
            
        data = response.json()
        resp_text = data.get("response", "").lower()
        metadata = data.get("metadata", [])
        
        # Check for shops
        has_coles = "coles" in resp_text
        has_woolworths = "woolworths" in resp_text
        
        # Check images
        image_urls = [m.get("image_url", "") for m in metadata if m.get("image_url")]
        
        # Simple heuristic verify
        image_matches = []
        if image_urls:
            for url in image_urls:
                if product.lower() in url.lower():
                    image_matches.append(True)
                else:
                    image_matches.append(False)
            any_image_match = any(image_matches)
        else:
            any_image_match = False
        
        return {
            "product": product,
            "status": "OK",
            "coles": "YES" if has_coles else "NO",
            "woolworths": "YES" if has_woolworths else "NO",
            "images": len(image_urls),
            "image_match": "YES" if any_image_match else ("NO" if image_urls else "N/A"),
            "duration": duration,
            "raw_images": image_urls
        }
        
    except Exception as e:
        return {
            "product": product,
            "status": "EXCEPTION",
            "coles": "N/A",
            "woolworths": "N/A",
            "images": 0,
            "image_match": str(e)[:20],
            "duration": time.time() - start_time,
            "raw_images": []
        }

async def main():
    print(f"Starting Product & Image Verification against {API_URL}")
    print("-" * 80)
    header = f"{'Product':<12} | {'Status':<8} | {'Coles':<5} | {'Wool':<5} | {'Imgs':<4} | {'Match':<5} | {'Time':<6}"
    print(header)
    print("-" * 80)
    
    results = []
    
    async with httpx.AsyncClient() as client:
        for i, product in enumerate(PRODUCTS, 1):
            res = await verify_product(client, product, i)
            results.append(res)
            
            # Print immediate result
            dur_val = res['duration']
            dur_str = f"{dur_val:.1f}s" if isinstance(dur_val, (int, float)) else str(dur_val)
            # Truncate status if too long
            status_str = res['status'][:8]
            
            row = f"{res['product']:<12} | {status_str:<8} | {res['coles']:<5} | {res['woolworths']:<5} | {str(res['images']):<4} | {res['image_match']:<5} | {dur_str:<6}"
            print(row)
            
    # Save detailed results
    with open("verification_results.json", "w") as f:
        serializable = []
        for r in results:
            rc = r.copy()
            if isinstance(rc['duration'], (int, float)):
                rc['duration'] = f"{rc['duration']:.2f}s"
            serializable.append(rc)
        json.dump(serializable, f, indent=2)
    print(f"\nDetailed results saved to verification_results.json")

if __name__ == "__main__":
    asyncio.run(main())
