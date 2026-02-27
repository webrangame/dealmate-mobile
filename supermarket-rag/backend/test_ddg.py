import httpx
from bs4 import BeautifulSoup
import asyncio
import re

async def search_api():
    search_url = "https://html.duckduckgo.com/html/?q=site:woolworths.com.au/shop/catalogue/view filetype:pdf"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False) as client:
        try:
            resp = await client.get(search_url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for a in soup.find_all('a', class_='result__url'):
                href = a.get('href', '')
                if 'pdf' in href.lower() or 'catalogue' in href.lower():
                    print("Found URL:", a.text.strip())
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(search_api())
