#!/usr/bin/env python3
"""
Trigger production ingestion and run 20x20 test
"""
import os
import subprocess
import time
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com"
ADMIN_KEY = os.getenv("ADMIN_API_KEY")

async def trigger_ingestion():
    """Trigger production ingestion"""
    if not ADMIN_KEY:
        print("❌ ADMIN_API_KEY not found in .env file")
        return False
    
    print("=" * 80)
    print("TRIGGERING PRODUCTION INGESTION")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print()
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            print("Sending ingestion request...")
            response = await client.post(
                f"{API_URL}/api/admin/ingest",
                headers={
                    "X-Admin-Key": ADMIN_KEY,
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Ingestion successful!")
                print(f"Response: {result}")
                return True
            else:
                print(f"❌ Ingestion failed: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    # Step 1: Trigger ingestion
    success = await trigger_ingestion()
    
    if not success:
        print("\n⚠️  Ingestion failed. Skipping tests.")
        return
    
    # Wait a bit for ingestion to settle
    print("\nWaiting 10 seconds for ingestion to settle...")
    await asyncio.sleep(10)
    
    # Step 2: Run 20x20 test
    print("\n" + "=" * 80)
    print("RUNNING 20x20 LIVE TEST")
    print("=" * 80)
    print()
    
    subprocess.run(["python3", "test_20x20_live.py"])

if __name__ == "__main__":
    asyncio.run(main())
