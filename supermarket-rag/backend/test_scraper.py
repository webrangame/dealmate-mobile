import httpx
from bs4 import BeautifulSoup
import asyncio

async def test_woolworths():
    url = "https://www.woolworths.com.au/shop/catalogue"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False) as client:
        try:
            resp = await client.get(url)
            print(resp.status_code)
            soup = BeautifulSoup(resp.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for l in links:
                if 'pdf' in l['href'].lower() or 'download' in l['href'].lower() or 'catalogue' in l['href'].lower():
                    print(l['href'])
            
            # Look for script tags with JSON
            for script in soup.find_all('script'):
                if script.string and 'catalog' in script.string.lower() and 'pdf' in script.string.lower():
                    print("Found potentially interesting script tag")
                    # print(script.string[:200])
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(test_woolworths())
