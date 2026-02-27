import httpx
import asyncio
from bs4 import BeautifulSoup

async def find_pdf():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    # Try the Woolworths API endpoints to get catalogue info
    # Sometimes the specials API exposes the catalogue URL
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False, timeout=10.0) as client:
        # Try the Everyday Rewards/specials API
        endpoints = [
            "https://www.woolworths.com.au/apis/ui/publication/v1", 
            "https://www.woolworths.com.au/api/v3/ui/catalogues",
            "https://www.woolworths.com.au/shop/catalogue",
        ]
        for url in endpoints:
            try:
                resp = await client.get(url)
                print(f"{url}: {resp.status_code}")
                if resp.status_code == 200:
                    print(resp.text[:200])
            except Exception as e:
                print(f"{url}: Error - {e}")
    
asyncio.run(find_pdf())
