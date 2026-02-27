import httpx
import asyncio

async def search_api():
    # Another common endpoint for Australian catalogues is Salefinder
    url = "https://embed.salefinder.com.au/catalogue/svgData/126" # 126 is often Woolworths on salefinder
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False) as client:
        try:
            resp = await client.get(url)
            print("Status:", resp.status_code)
            # print(resp.text[:500])
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(search_api())
