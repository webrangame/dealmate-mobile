#!/usr/bin/env python3
"""
Manual catalog downloader - use when auto_update_catalogs.py fails
"""
import asyncio
import httpx
import os

UPLOAD_DIR = "uploaded_docs"

async def download_catalog(url, filename):
    """Download a catalog PDF"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    print(f"Downloading {filename}...")
    print(f"URL: {url}")
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=120.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                size_mb = len(resp.content) / (1024 * 1024)
                print(f"✓ Downloaded {filename} ({size_mb:.1f} MB)")
                return filepath
            else:
                print(f"✗ Failed: HTTP {resp.status_code}")
                return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

async def main():
    # Current week URLs (Feb 11-17, 2026)
    catalogs = [
        ("https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/WW_NSW_110226_5UK7TA7434.pdf", "Woolworths.pdf"),
        # Coles URL needs to be updated manually - check SaleFinder or use existing file
    ]
    
    print("=" * 60)
    print("MANUAL CATALOG DOWNLOADER")
    print("=" * 60)
    print()
    
    for url, filename in catalogs:
        await download_catalog(url, filename)
        print()
    
    print("=" * 60)
    print("NEXT STEPS:")
    print("1. For Coles: Visit https://salefinder.com.au/Coles-catalogue")
    print("   - Find the NSW METRO catalogue")
    print("   - Check browser DevTools Network tab for PDF URL")
    print("   - Download manually and save as 'Coles.pdf'")
    print()
    print("2. Run ingestion:")
    print("   python3 manual_ingest.py")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
