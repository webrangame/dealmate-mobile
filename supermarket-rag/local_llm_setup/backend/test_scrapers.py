import asyncio
import httpx
import re

COLES_CATALOG_URL = "https://www.coles.com.au/catalogues"
WOOLWORTHS_CATALOG_URL = "https://www.woolworths.com.au/shop/catalogue/view"

async def test_scrapers():
    print("Testing Coles Scraper...")
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            resp = await client.get(COLES_CATALOG_URL, headers=headers)
            print(f"Coles Response Status: {resp.status_code}")
            pdf_links = re.findall(r'https?://[^\s"\'<>]+?\.pdf', resp.text)
            print(f"Found {len(pdf_links)} PDF links on Coles.")
            for link in pdf_links:
                if "COL" in link.upper() and "METRO" in link.upper():
                    print(f"MATCH: {link}")
        except Exception as e:
            print(f"Coles Test Failed: {e}")

    print("\nTesting Woolworths Scraper...")
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.get(WOOLWORTHS_CATALOG_URL, headers=headers)
            print(f"Woolworths Response Status: {resp.status_code}")
            pdf_links = re.findall(r'https?://[^\s"\'<>]+?\.pdf', resp.text)
            print(f"Found {len(pdf_links)} PDF links on Woolworths.")
            for link in pdf_links:
                if "WW_" in link.upper() and ("NSW" in link.upper() or "VIC" in link.upper()):
                    print(f"MATCH: {link}")
    except Exception as e:
        print(f"Woolworths Test Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_scrapers())
