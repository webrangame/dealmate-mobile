import asyncio
import httpx
import json
import sys
import time

# Configuration - hitting the local port 8002
API_BASE_URL = "http://localhost:8002"
CHAT_ENDPOINT = f"{API_BASE_URL}/chat"

# 20 Product Questions
PRODUCT_QUESTIONS = [
    "What is the price of Arnott's Shapes at Coles?",
    "How much is Devondale Milk Powder at Woolworths?",
    "Show me deals for Coca-Cola 30 pack.",
    "Best price for Ice Cream at Coles?",
    "Price of Pak Choy at Coles?",
    "Is there any discount on Cadbury Dairy Milk at Woolworths?",
    "Cost of Australian Premium Strawberries at Coles?",
    "How much for Annalisa Tomatoes at Woolworths?",
    "Price of Tim Tam at Coles?",
    "Deals on laundry detergent at Woolworths?",
    "Price of Bread at Coles?",
    "How much is Butter at Woolworths?",
    "Price of Eggs 12 pack at Coles?",
    "Deals on Chicken Breast at Woolworths?",
    "Price of Bananas at Coles?",
    "How much is Toilet Paper at Woolworths?",
    "Price of Pavlova base at Coles?",
    "Deals on Coffee pods at Woolworths?",
    "Price of Olive Oil 1L at Coles?",
    "How much is Rice 5kg at Woolworths?"
]

# 20 General Questions
GENERAL_QUESTIONS = [
    "Hello",
    "Who are you?",
    "How do you help customers?",
    "What supermarkets do you compare?",
    "Tell me a joke.",
    "What is the capital of Australia?",
    "How can I save money on groceries?",
    "What are the benefits of comparing prices?",
    "Do you have any recipes for pasta?",
    "Where is the nearest Coles?",
    "Is Woolworths cheaper than Coles usually?",
    "Thank you for the help.",
    "What is your name?",
    "Can you help me find cheap milk?",
    "What are rewards cards?",
    "How often do prices change?",
    "What is Niyogen?",
    "Can I buy things directly through you?",
    "What's the weather like?",
    "Goodbye"
]

async def call_api(client, q, user_id):
    try:
        response = await client.post(CHAT_ENDPOINT, json={"text": q, "user_id": user_id}, timeout=60.0)
        if response.status_code == 200:
            data = response.json()
            resp_text = data.get("response", "")
            if resp_text and len(resp_text) > 5:
                return True, len(resp_text)
            return False, "Empty response"
        return False, f"Status {response.status_code}"
    except Exception as e:
        return False, str(e)

async def run_batch(questions, category, semaphore, client):
    async def limited_call(q, i):
        async with semaphore:
            res, detail = await call_api(client, q, f"mass_test_{category.lower()}_{i}")
            status = "[OK]" if res else f"[FAILED] {detail}"
            print(f"[{category}] Query {i+1}: {q[:30]}... -> {status}")
            return res

    tasks = [limited_call(q, i) for i, q in enumerate(questions)]
    results = await asyncio.gather(*tasks)
    return sum(1 for r in results if r)

async def main():
    print("STARTING PARALLEL LOCAL MASS TEST (40 QUESTIONS)")
    start_time = time.time()
    semaphore = asyncio.Semaphore(5) # Run 5 at a time
    
    async with httpx.AsyncClient() as client:
        p_success = await run_batch(PRODUCT_QUESTIONS, "PRODUCT", semaphore, client)
        g_success = await run_batch(GENERAL_QUESTIONS, "GENERAL", semaphore, client)
    
    end_time = time.time()
    print("\n" + "="*40)
    print(f"FINAL RESULTS (Duration: {end_time - start_time:.1f}s)")
    print(f"Product Questions: {p_success}/20")
    print(f"General Questions: {g_success}/20")
    print(f"Overall: {p_success + g_success}/40")
    print("="*40)

if __name__ == "__main__":
    asyncio.run(main())
