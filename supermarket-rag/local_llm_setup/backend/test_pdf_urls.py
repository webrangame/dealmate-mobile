#!/usr/bin/env python3
"""Quick test to verify catalog PDF URLs are accessible"""
import asyncio
import httpx

async def test_pdf_urls():
    urls = {
        "Coles NSW Metro": "https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/COLNSWMETRO_110226_AQH86RS.pdf",
        "Woolworths NSW": "https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/WW_NSW_110226_5UK7TA7434.pdf"
    }
    
    print("Testing catalog PDF URLs...\n")
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        for name, url in urls.items():
            try:
                resp = await client.head(url)
                size_mb = int(resp.headers.get('content-length', 0)) / (1024 * 1024)
                if resp.status_code == 200:
                    print(f"✓ {name}: ACCESSIBLE ({size_mb:.1f} MB)")
                else:
                    print(f"✗ {name}: HTTP {resp.status_code}")
            except Exception as e:
                print(f"✗ {name}: ERROR - {e}")

if __name__ == "__main__":
    asyncio.run(test_pdf_urls())
