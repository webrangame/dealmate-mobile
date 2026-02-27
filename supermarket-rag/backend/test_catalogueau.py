import httpx
import asyncio
from bs4 import BeautifulSoup
import re

async def get_woolworths_pdf_via_catalogueau(region="NSW"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False, timeout=10.0) as client:
        # catalogueau.com lists woolworths catalogues
        url = f"https://www.catalogueau.com/Woolworths"
        resp = await client.get(url)
        print("Status:", resp.status_code)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Search for NSW catalogue links
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.get_text()
                if 'NSW' in text or 'NSW' in href:
                    print(f"Found NSW link: {text.strip()} | {href}")
            # Broader search
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'woolworths' in href.lower() or 'catalogue' in href.lower():
                    text = a.get_text()
                    print(f"Catalogue link: {text.strip()[:50]} | {href}")
                    break

asyncio.run(get_woolworths_pdf_via_catalogueau())
