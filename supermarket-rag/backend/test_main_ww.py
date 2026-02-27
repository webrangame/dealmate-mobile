import httpx
import asyncio
from bs4 import BeautifulSoup
import re

async def get_woolworths_pdf():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False, timeout=10.0) as client:
        # The woolworths main page on catalogueau
        url = "https://www.catalogueau.com/woolworths/"
        resp = await client.get(url)
        print("Status:", resp.status_code)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Look for script tags that may contain PDF info
            for script in soup.find_all('script'):
                if script.string and ('pdf' in script.string.lower() or d3vvi2v9g := ('d3vvi' in script.string)):
                    print("Found script with pdf/cdn:", script.string[:300])
            
            # Look for iframes (catalogue viewers typically use iframes)
            for iframe in soup.find_all('iframe'):
                print("Iframe src:", iframe.get('src', ''))
            
            # Look for download links
            for a in soup.find_all('a', href=True):
                href = a['href']
                if '.pdf' in href.lower() or 'download' in href.lower():
                    print("Download link:", href)
    
asyncio.run(get_woolworths_pdf())
