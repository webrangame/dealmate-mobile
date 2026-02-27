import httpx
import asyncio
from datetime import datetime, timedelta
import string
import itertools
import random

def get_recent_wednesdays():
    now = datetime.now()
    dates = []
    days_to_sub = (now.weekday() - 2) % 7
    latest = now - timedelta(days=days_to_sub)
    dates.append(latest.strftime("%d%m%y"))
    prev = latest - timedelta(days=7)
    dates.append(prev.strftime("%d%m%y"))
    return dates

async def test_cdn_patterns():
    """Try different patterns for Woolworths CDN URLs."""
    date_codes = get_recent_wednesdays()
    print("Checking dates:", date_codes)
    
    # The current suffixes seem invalid, let's try the same structure but different
    # Woolworths catalogue URL formats commonly seen online
    
    # Format: https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/WW_NSW_{dateCode}_{suffix}.pdf
    # Old suffixes: 5UK7TA7434, 5UK7TA8545, 5UK7TA1122
    # Let's try variations
    
    # Also try alternate CDNs and URL patterns
    base_patterns = [
        "https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/WW_NSW_{date}_{suffix}.pdf",
        "https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/WW-NSW-{date}-{suffix}.pdf",
        "https://d3vvi2v9oj75wh.cloudfront.net/catalogues/WW_NSW_{date}_{suffix}.pdf",
        "https://d3vvi2v9oj75wh.cloudfront.net/pdf/WW_NSW_{date}_{suffix}.pdf",
    ]
    
    # Try some common suffix pattern variations
    # Woolworths usually has format like 5UK7TA followed by 4 digits
    # Let's try the pattern with a wider range
    common_suffixes = [
        # Original 
        "5UK7TA7434", "5UK7TA8545", "5UK7TA1122",
        # Some variations  
        "5UK7TA0001", "5UK7TA1234", "5UK7TA2345", "5UK7TA3456",
        "5UK7TA4567", "5UK7TA5678", "5UK7TA6789", "5UK7TA9876",
        # Completely different codes
        "6UK7TA7434", "5VK7TA7434", "5UK8TA7434",
        # No suffix (just date)
        "",
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, verify=False, timeout=5.0) as client:
        for date_code in date_codes:
            for suffix in common_suffixes:
                for pattern in base_patterns[:1]:  # Just try the main pattern first
                    url = pattern.format(date=date_code, suffix=suffix)
                    try:
                        resp = await client.head(url)
                        print(f"[{resp.status_code}] {url}")
                        if resp.status_code == 200:
                            print("*** FOUND VALID URL! ***")
                            return url
                    except Exception as e:
                        pass

asyncio.run(test_cdn_patterns())
