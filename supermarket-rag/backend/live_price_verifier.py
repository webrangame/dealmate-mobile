import os
import httpx
import asyncio
from bs4 import BeautifulSoup
import re
import time
from typing import Dict, Optional

class LivePriceVerifier:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.zenrows_url = "https://api.zenrows.com/v1/"
        self.cache = {} # Basic in-memory cache: { "product_shop": {"price": "...", "timestamp": ...} }
        self.cache_duration = 3600 * 4 # Cache for 4 hours
        
    async def get_live_price(self, product_name: str, shop: str) -> Optional[Dict]:
        """
        Uses ZenRows to fetch the latest price for a product from a specific shop.
        Uses caching to avoid redundant calls.
        """
        cache_key = f"{product_name}_{shop}".lower()
        now = time.time()
        
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if now - entry['timestamp'] < self.cache_duration:
                print(f"DEBUG: Using cached price for {product_name}")
                return entry['data']
        search_query = f"{product_name} {shop} Australia"
        
        # 1. Search for the product URL using a search engine (mimicking a user finding the page)
        # For simplicity and robustness, we'll try to guess/search the direct store URL if possible
        # but starting with a search is more reliable for varied naming.
        
        if "woolworths" in shop.lower():
            target_url = f"https://woolworths.com.au/shop/search/products?searchTerm={product_name.replace(' ', '%20')}"
        elif "coles" in shop.lower():
            target_url = f"https://www.coles.com.au/search?q={product_name.replace(' ', '%20')}"
        else:
            return {"status": "error", "message": f"Unsupported shop: {shop}"}

        # Store-specific overrides
        js_render = "true" 
        wait_for = None # Default to None for non-supermarket sites
        
        if "coles" in shop.lower():
            wait_for = ".price, .coles-targeting-ProductTilePrice"
        elif "woolworths" in shop.lower():
            wait_for = ".product-tile-price, .primary"

        # Determine proxy country and premium status based on domain
        # Supermarket sites (Coles/Woolworths) need Australian proxies.
        # General sites like httpbin.org usually work better with US premium proxies.
        proxy_country = "au"
        premium_proxy = "true"
        
        if "httpbin.org" in target_url:
            proxy_country = "us"
            premium_proxy = "true"
            
        params = {
            "apikey": self.api_key,
            "url": target_url,
            "js_render": js_render,
            "premium_proxy": premium_proxy,
            "proxy_country": proxy_country
        }

        try:
            print(f"DEBUG: Requesting {target_url} via ZenRows (JS={js_render}, 300s Timeout)...")
            async with httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=15.0)) as client:
                response = await client.get(self.zenrows_url, params=params)
                
                print(f"DEBUG: ZenRows Status: {response.status_code}")
                if response.status_code != 200:
                    print(f"DEBUG: Error Response Content: {response.text[:500]}")
                    return {"status": "error", "message": f"ZenRows Error: {response.status_code}"}
                
                print(f"DEBUG: Successfully fetched page. Length: {len(response.text)}")
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Specialized extraction logic
                if "woolworths" in shop.lower():
                    price = self._extract_woolworths_price(soup)
                else:
                    price = self._extract_coles_price(soup)
                    
                if price:
                    result = {
                        "price": price, 
                        "url": target_url, 
                        "status": "success",
                        "product_verified": product_name
                    }
                    # Store in cache
                    self.cache[cache_key] = {
                        "timestamp": now,
                        "data": result
                    }
                    return result
                else:
                    return {"status": "not_found", "url": target_url}
                    
        except Exception as e:
            import traceback
            print(f"DEBUG: Exception in get_live_price: {traceback.format_exc()}")
            return {"status": "error", "message": f"{type(e).__name__}: {str(e)}"}

    def _extract_woolworths_price(self, soup):
        # 1. Standard CSS Selectors
        price_tag = soup.select_one(".primary")
        if not price_tag:
            price_tag = soup.select_one(".product-tile-price")
        if not price_tag:
            price_tag = soup.select_one(".price, .shared-price")
            
        if price_tag:
            text = price_tag.get_text(strip=True)
            if "$" in text: return text

        # 2. JSON-LD Fallback (Very common for supermarket products)
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                import json
                data = json.loads(script.string)
                # handle list of items or single item
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if item.get("@type") == "Product" or "offers" in item:
                        offers = item.get("offers", {})
                        if isinstance(offers, dict):
                            price = offers.get("lowPrice") or offers.get("price")
                            if price: return f"${price}"
            except:
                continue

        # 3. Meta tag Fallback
        meta_price = soup.find("meta", property="product:price:amount")
        if meta_price:
            return f"${meta_price.get('content')}"

        # 4. Fallback: Search all text for first price-like string after find product name?
        # Too risky for now.
        return None

    def _extract_coles_price(self, soup):
        # Coles price extraction
        price_tag = soup.select_one(".price, .coles-targeting-ProductTilePrice")
        if price_tag:
            return price_tag.get_text(strip=True)
        return None

# Simple CLI test
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    key = os.getenv("ZENROWS_API_KEY")
    if not key:
        print("Set ZENROWS_API_KEY in .env")
    else:
        verifier = LivePriceVerifier(key)
        async def main():
            result = await verifier.get_live_price("Connoisseur Ice Cream 1 Litre", "Woolworths")
            print(result)
        asyncio.run(main())
