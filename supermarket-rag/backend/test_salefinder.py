import httpx
import asyncio
import json

async def get_woolworths_catalogue():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False) as client:
        # Try salefinder API for woolworths catalogues
        url = "https://embed.salefinder.com.au/api/outlets/list/126"
        resp = await client.get(url)
        print("Outlets status:", resp.status_code)
        if resp.status_code == 200:
            print(resp.text[:500])
        
        # Try catalogue list for woolworths
        url2 = "https://embed.salefinder.com.au/api/catalogues/list/126"
        resp2 = await client.get(url2)
        print("Catalogues status:", resp2.status_code)
        if resp2.status_code == 200:
            print(resp2.text[:800])

asyncio.run(get_woolworths_catalogue())
