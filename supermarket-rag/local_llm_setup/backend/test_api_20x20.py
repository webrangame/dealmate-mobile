import asyncio
import httpx
import json
import time
from datetime import datetime

# API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat" # Old URL from 10x10 test
# Need to confirm if this is still the active one or if user needs to deploy first.
# Assuming same URL for now, but will make it configurable.
import os
API_URL = os.getenv("API_URL", "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat")
USER_ID = "test_user_20x20@gmail.com"

GENERAL_QUESTIONS = [
    "Hello", "Good morning", "Who are you?", "What can you do?", "How does this app work?",
    "Thanks", "What is the weather usually like?", "Tell me a joke", "What time is it?", "Goodbye",
    "Are you a human?", "Where are you hosted?", "Can you cook?", "What is your name?", "Help me",
    "I need assistance", "Hi there", "Good evening", "What stores do you check?", "Is this free?"
]

PRODUCT_QUESTIONS = [
    "Price of milk", "How much is Coca Cola?", "Cheapest bread", "Cost of bananas", "Price of eggs",
    "Woolworths pasta sauce", "Cadbury chocolate", "Price of Tim Tams", "Frozen chips price", "Toilet paper price",
    "Nescafe coffee price", "Best deal on rice", "Price of chicken breast", "Coles ice cream", "Olive oil cost",
    "Detergent price", "Shampoo deals", "Dog food price", "Cat food specials", "Butter usage"
]

async def test_question(client, question, q_id, q_type):
    print(f"[{q_id}] {q_type}: {question}")
    start = time.time()
    try:
        resp = await client.post(API_URL, json={"text": question, "user_id": USER_ID}, timeout=60.0)
        dur = time.time() - start
        return {
            "id": q_id, "type": q_type, "question": question, 
            "status": resp.status_code, "duration": round(dur, 2), 
            "response": resp.json() if resp.status_code == 200 else resp.text
        }
    except Exception as e:
        return {"id": q_id, "type": q_type, "question": question, "status": 0, "error": str(e), "duration": round(time.time() - start, 2)}

async def run():
    print(f"Starting 20x20 Test against {API_URL}")
    results = []
    async with httpx.AsyncClient() as client:
        for i, q in enumerate(GENERAL_QUESTIONS):
            results.append(await test_question(client, q, i+1, "General"))
            # await asyncio.sleep(1)
        for i, q in enumerate(PRODUCT_QUESTIONS):
            results.append(await test_question(client, q, i+21, "Product"))
            # await asyncio.sleep(1)
            
    with open("test_results_20x20.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Tests Completed. Results saved to test_results_20x20.json")

if __name__ == "__main__":
    asyncio.run(run())
