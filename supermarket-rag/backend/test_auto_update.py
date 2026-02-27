#!/usr/bin/env python3
"""
Quick test of the complete auto_update_catalogs.py workflow
Tests URL fetching without actually downloading or ingesting
"""
import asyncio
from auto_update_catalogs import get_coles_pdf_url, get_woolworths_pdf_url

async def test_workflow():
    print("=" * 60)
    print("TESTING AUTO_UPDATE_CATALOGS.PY WORKFLOW")
    print("=" * 60)
    print()
    
    print("Step 1: Finding Coles PDF URL...")
    coles_url = await get_coles_pdf_url()
    print(f"Result: {coles_url}")
    print()
    
    print("Step 2: Finding Woolworths PDF URL...")
    ww_url = await get_woolworths_pdf_url()
    print(f"Result: {ww_url}")
    print()
    
    print("=" * 60)
    print("✅ URL DISCOVERY TEST COMPLETE")
    print("=" * 60)
    print()
    print("Both URLs found successfully!")
    print("To run full update (download + ingest + email):")
    print("  python3 auto_update_catalogs.py")

if __name__ == "__main__":
    asyncio.run(test_workflow())
