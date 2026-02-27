import httpx
import asyncio
import json

BASE_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com"
ADMIN_KEY = "5ab868c201588d172fdbe7f3e627098dc451d1cff012e03923f07f3889f03b0e"

async def test_apis():
    async with httpx.AsyncClient(timeout=60.0) as client:
        results = {}

        # 1. Health Check
        print("Testing /health...")
        resp = await client.get(f"{BASE_URL}/health")
        results["health"] = {"status": resp.status_code, "body": resp.json()}

        # 2. Chat (Single Item)
        print("Testing /chat (Single Item)...")
        chat_data = {"text": "price of milk", "user_id": "test_user_prod"}
        resp = await client.post(f"{BASE_URL}/chat", json=chat_data)
        results["chat_single"] = {"status": resp.status_code, "body": resp.json() if resp.status_code == 200 else resp.text}

        # 3. Chat (Multi Item) - THE NEW FEATURE
        print("Testing /chat (Multi Item)...")
        chat_data_multi = {"text": "ice cream and rice", "user_id": "test_user_prod"}
        resp = await client.post(f"{BASE_URL}/chat", json=chat_data_multi)
        results["chat_multi"] = {"status": resp.status_code, "body": resp.json() if resp.status_code == 200 else resp.text}

        # 4. Get Items
        print("Testing /api/items...")
        resp = await client.get(f"{BASE_URL}/api/items?shop_name=Coles&limit=5")
        results["get_items"] = {"status": resp.status_code, "body": resp.json() if resp.status_code == 200 else resp.text}

        # 5. Admin Ingest (Check Auth)
        print("Testing /api/admin/ingest (Auth Check)...")
        headers = {"Authorization": f"Bearer {ADMIN_KEY}"}
        resp = await client.post(f"{BASE_URL}/api/admin/ingest", headers=headers)
        results["admin_ingest"] = {"status": resp.status_code, "body": resp.json() if resp.status_code == 200 else resp.text}

        print("\n--- Summary ---")
        for api, res in results.items():
            print(f"{api}: Status {res['status']}")

        with open("production_api_test_results.json", "w") as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    asyncio.run(test_apis())
