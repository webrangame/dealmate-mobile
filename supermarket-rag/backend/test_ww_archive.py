import httpx
import asyncio
from bs4 import BeautifulSoup
import re

async def get_woolworths_pdf():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False, timeout=10.0) as client:
        # Get the woolworths archive page
        url = "https://www.catalogueau.com/woolworths-archive/"
        resp = await client.get(url)
        print("Status:", resp.status_code)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Print all links - look for catalogue links with recent dates
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.get_text().strip()
                if text and ('2025' in text or '2026' in text or 'woolworths' in href.lower()):
                    print(f"Link: {text[:70]} -> {href}")
            
asyncio.run(get_woolworths_pdf())
