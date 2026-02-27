import httpx
import asyncio
import json

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"
USER_ID = "final_verification_user"

async def test_query(text):
    print(f"\n>>> Querying: {text}")
    payload = {"text": text, "user_id": USER_ID}
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(API_URL, json=payload)
        if resp.status_code == 200:
            print(resp.json()["response"])
        else:
            print(f"FAILED: {resp.status_code} - {resp.text}")

async def main():
    queries = [
        "What is the price of Radiant Laundry Capsules in Coles?",
        "Do you have Canadian Club in Coles? List the price and deal.",
        "Show me prices for cat food and list some deals.",
        "What is the price of Dine Cat Food?"
    ]
    for q in queries:
        await test_query(q)

if __name__ == "__main__":
    asyncio.run(main())
