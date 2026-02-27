import httpx
import asyncio
import json
import re

async def search_woolworths_pdf():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False, timeout=10.0) as client:
        # Try Shopfully/Tiendeo API - Australian catalogues
        url = "https://au.shopfully.io/api/v2/flyers?store_id=woolworths&zone_code=NSW"
        resp = await client.get(url)
        print("Shopfully status:", resp.status_code)
        if resp.status_code == 200:
            print(resp.text[:500])
        
asyncio.run(search_woolworths_pdf())
