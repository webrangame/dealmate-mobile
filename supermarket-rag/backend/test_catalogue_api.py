import httpx
import asyncio

async def search_api():
    # Woolworths actually uses a specific API for its catalogues
    # Let's see if we can query it
    
    url = "https://www.woolworths.com.au/api/v3/ui/schema/delivery-options"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    # Or maybe there's a catalogue API endpoint
    # Like https://petals.woolworths.com.au/catalogue/
    
    # Let's try to query Google for the latest PDF URL
    search_url = "https://html.duckduckgo.com/html/?q=site:woolworths.com.au/shop/catalogue/view filetype:pdf"
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False) as client:
        try:
            resp = await client.get(search_url)
            print("Status:", resp.status_code)
            print(resp.text[:500])
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(search_api())
