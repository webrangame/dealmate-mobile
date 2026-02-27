import httpx
import asyncio
from bs4 import BeautifulSoup
import re

async def get_woolworths_pdf_via_catalogueau(region="NSW"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False, timeout=10.0) as client:
        # Look for the weekly catalogue page
        url = f"https://www.catalogueau.com/Woolworths-Catalogue"
        resp = await client.get(url)
        print("Status:", resp.status_code)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Print all links
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.get_text().strip()
                if text and len(text) > 3:
                    print(f"Link: {text[:60]} -> {href}")
            
asyncio.run(get_woolworths_pdf_via_catalogueau())
