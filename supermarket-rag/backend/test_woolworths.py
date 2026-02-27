import asyncio
import httpx
from datetime import datetime, timedelta

def get_recent_wednesdays():
    now = datetime.now()
    dates = []
    days_to_sub = (now.weekday() - 2) % 7
    latest = now - timedelta(days=days_to_sub)
    dates.append(latest.strftime("%d%m%y"))
    prev = latest - timedelta(days=7)
    dates.append(prev.strftime("%d%m%y"))
    return dates

async def get_woolworths_pdf_url(region="NSW"):
    date_codes = get_recent_wednesdays()
    suffixes = ["5UK7TA7434", "5UK7TA8545", "5UK7TA1122"]
    region_map = {
        "NSW": "WW_NSW",
        "VIC": "WW_VIC",
        "QLD": "WW_QLD",
        "WA": "WW_WA"
    }
    prefix = region_map.get(region, "WW_NSW")
    async with httpx.AsyncClient(follow_redirects=True, timeout=5.0) as client:
        for date_code in date_codes:
            print(f"Checking Woolworths {region} for date {date_code}...")
            for suffix in suffixes:
                url = f"https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/{prefix}_{date_code}_{suffix}.pdf"
                try:
                    resp = await client.head(url)
                    print(url, resp.status_code)
                    if resp.status_code == 200:
                        print(f"✓ Found Woolworths {region} PDF: {url}")
                        return url
                except Exception as e:
                    print("Error", e)
                    continue
    return None

asyncio.run(get_woolworths_pdf_url("NSW"))
