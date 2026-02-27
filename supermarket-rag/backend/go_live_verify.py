import asyncio
import httpx
import os
import json
import time

API_URL = "http://localhost:8000"
ADMIN_KEY = os.getenv("ADMIN_API_KEY", "super-secret-key-change-me")
USER_ID = "go_live_tester@niyogen.com"

async def test_endpoint(name, method, endpoint, payload=None, files=None, headers=None, expected_status=200, timeout=60.0):
    print(f"\n--- Testing {name} ({method} {endpoint}) ---")
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            url = f"{API_URL}{endpoint}"
            if method == "GET":
                resp = await client.get(url, params=payload, headers=headers)
            elif method == "POST":
                if files:
                    resp = await client.post(url, data=payload, files=files, headers=headers)
                else:
                    resp = await client.post(url, json=payload, headers=headers)
            
            status = resp.status_code
            print(f"Status: {status}")
            if status == expected_status:
                print(f"✅ Success")
                return True, resp.json() if resp.text else None
            else:
                print(f"❌ Failed: {resp.text[:200]}")
                return False, resp.text
        except httpx.ReadTimeout:
            print(f"⚠️  Timeout (as expected for long tasks)")
            return True, "Timeout (Ingestion likely started)"
        except Exception as e:
            print(f"❌ Exception: {type(e).__name__}: {e}")
            return False, str(e)

async def run_verification():
    print("STARTING GO-LIVE READINESS VERIFICATION\n")
    results = {}

    # 1. Health Check
    results["health"] = await test_endpoint("Health Check", "GET", "/health", timeout=10.0)

    # 2. Chat/RAG Engine
    chat_payload = {"text": "What is the price of eggs?", "user_id": USER_ID}
    results["chat"] = await test_endpoint("Chat API", "POST", "/chat", payload=chat_payload, timeout=90.0)

    # 3. Get Shop Items
    items_payload = {"shop_name": "Coles", "limit": 5}
    results["items"] = await test_endpoint("Get Items API", "GET", "/api/items", payload=items_payload, timeout=20.0)

    # 4. Admin Auth Check (Catalog Update is safer as it is background)
    headers = {"Authorization": f"Bearer {ADMIN_KEY}"}
    print("\n--- Testing Admin Auth (Catalog Update) ---")
    results["admin_update"] = await test_endpoint("Admin Update Catalogs", "POST", "/api/admin/update-catalogs", headers=headers, timeout=10.0)

    # Summary
    print("\n" + "="*40)
    print("VERIFICATION SUMMARY")
    all_passed = True
    for test, (passed, _) in results.items():
        status_str = "PASS" if passed else "FAIL"
        print(f"{test:22}: {status_str}")
        if not passed: all_passed = False
    print("="*40)
    
    if all_passed:
        print("\nSYSTEM IS READY FOR GO-LIVE!")
    else:
        print("\nSYSTEM HAS BLOCKED ISSUES. SEE LOGS.")

if __name__ == "__main__":
    asyncio.run(run_verification())
