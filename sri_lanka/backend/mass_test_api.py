import asyncio
import httpx
import json
import os
import sys

# Configuration
API_BASE_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com"
CHAT_ENDPOINT = f"{API_BASE_URL}/chat"

# Test data (Product, Shop, Expected Price Substring, Expected Image URL)
TEST_CASES = [
    # Coles Items
    ("Arnott's Creams Biscuits", "Coles", "$3", "Coles_p25_item1"),
    ("Arnott's Marie or Nice Biscuits", "Coles", "$2", "Coles_p25_item0"),
    ("Arnott's Salada or Vita-Weat Crispbreads", "Coles", "$6", "Coles_p25_item2"),
    ("Arnott's Shapes Crackers", "Coles", "$2.00", "Coles_p1_item0"),
    ("Arnott's Shapes or Tiny Teddy", "Coles", "$6.00", "Coles_p26_item9"),
    ("Arnott's TeeVee Snacks or Wagon Wheels Biscuits", "Coles", "$3.30", "Coles_p26_item2"),
    ("Australian Buk Choy or Pak Choy", "Coles", "$5.00", "Coles_p16_item5"),
    ("Australian Petite Wombok 2 Pack", "Coles", "$4.50", "Coles_p20_item2"),
    ("Australian Premium Strawberries", "Coles", "$5.50", "Coles_p20_item4"),
    ("Ayam Sauce", "Coles", "$3.00", "Coles_p15_item4"),
    
    # Woolworths Items
    ("24ct Gold Plated Rose", "Woolworths", "$25", "Woolworths_p10_item7"),
    ("3 Tier Airer", "Woolworths", "$50", "Woolworths_p0_item9"),
    ("ABC Sweet Soy Ckecap Manis", "Woolworths", "$2.15", "Woolworths_p14_item2"),
    ("AJAX Eco Multipurpose Cleaner", "Woolworths", "$5.50", "Woolworths_p39_item1"),
    ("AJAX Floor Cleaner", "Woolworths", "$5.50", "Woolworths_p39_item4"),
    ("AIWA", "Woolworths", "$59", "Woolworths_p52_item7"),
    ("AIWA DGTEC", "Woolworths", "$149.25", "Woolworths_p53_item7"),
    ("Annalisa Tomatoes", "Woolworths", "$1.50", "Woolworths_p37_item0"),
    ("Arnott's Biscuit Tim Tam", "Woolworths", "$3.00", "Woolworths_p0_item2")
]

# Add one more Woolworths item to make it 20
TEST_CASES.append(("AJAX Spray n Wipe", "Woolworths", "$3.50", "Woolworths_p39_item5"))

async def test_query(product, shop, expected_price, img_snippet):
    query = f"What is the price of {product} at {shop}?"
    payload = {
        "text": query,
        "user_id": "mass_tester"
    }
    
    print(f"\n[TESTING] {product} at {shop}...", flush=True)
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(CHAT_ENDPOINT, json=payload)
            
            if response.status_code != 200:
                print(f"  [FAILED] Status Code: {response.status_code}", flush=True)
                return False
                
            data = response.json()
            resp_text = data.get("response", "").lower()
            metadata = data.get("metadata", [])
            
            # Check price
            price_found = expected_price.lower() in resp_text
            
            # Check image
            img_found = False
            for m in metadata:
                if img_snippet in m.get("image_url", ""):
                    img_found = True
                    break
            
            if price_found and img_found:
                print(f"  [SUCCESS] Price and Image verified.", flush=True)
                return True
            else:
                print(f"  [FAILED] Results: Price Match={price_found}, Image Match={img_found}", flush=True)
                if not price_found:
                    print(f"    Expected Price: {expected_price}", flush=True)
                if not img_found:
                    print(f"    Expected Image Snippet: {img_snippet}", flush=True)
                return False
                
    except Exception as e:
        print(f"  [ERROR] {e}", flush=True)
        return False

async def main():
    print("Starting Mass Test for 20 Production API Queries...", flush=True)
    results = []
    
    for product, shop, price, img in TEST_CASES:
        res = await test_query(product, shop, price, img)
        results.append(res)
        # Add a small delay to avoid overwhelming or triggering rate limits
        await asyncio.sleep(1)
        
    success_count = sum(1 for r in results if r)
    total_count = len(results)
    
    print("\n" + "="*40, flush=True)
    print(f"MASS TEST COMPLETED", flush=True)
    print(f"Total Tests: {total_count}", flush=True)
    print(f"Successful: {success_count}", flush=True)
    print(f"Failed: {total_count - success_count}", flush=True)
    print("="*40, flush=True)
    
    if success_count == total_count:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
