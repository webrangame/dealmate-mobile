import httpx
from bs4 import BeautifulSoup
import asyncio

async def test_woolworths():
    url = "https://www.woolworths.com.au/shop/catalogue/view"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False) as client:
        try:
            resp = await client.get(url)
            print("Status:", resp.status_code)
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Look at scripts
            for script in soup.find_all('script'):
                if script.string and 'window.wowCatalogue' in script.string:
                     print("Found window.wowCatalogue")
                     print(script.string[:500])
                     
            for script in soup.find_all('script'):
                if script.string and '.pdf' in script.string:
                     print("Found script with .pdf")
                     # print(script.string)
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(test_woolworths())
