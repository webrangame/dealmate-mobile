import asyncio
import httpx
import json
import sys

# Configuration - hitting the local port 8002
API_BASE_URL = "http://localhost:8000"
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

async def run_test(questions, category):
    print(f"\n--- Testing {category} Questions ---")
    success = 0
    for i, q in enumerate(questions):
        print(f"[{i+1}/20] Query: {q}")
        payload = {"text": q, "user_id": f"mass_test_{category.lower()}_{i}"}
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(CHAT_ENDPOINT, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    resp_text = data.get("response", "")
                    if resp_text and len(resp_text) > 5:
                        print(f"  [OK] Response received ({len(resp_text)} chars)")
                        success += 1
                    else:
                        print(f"  [ERROR] Empty or too short response.")
                else:
                    print(f"  [ERROR] Status {response.status_code}: {response.text}")
        except Exception as e:
            import traceback
            print(f"  [EXCEPTION] {e}")
            # traceback.print_exc()
        await asyncio.sleep(0.5)
    return success

async def main():
    print("STARTING LOCAL MASS TEST (40 QUESTIONS)")
    p_success = await run_test(PRODUCT_QUESTIONS, "PRODUCT")
    g_success = await run_test(GENERAL_QUESTIONS, "GENERAL")
    
    print("\n" + "="*40)
    print(f"FINAL RESULTS")
    print(f"Product Questions: {p_success}/20")
    print(f"General Questions: {g_success}/20")
    print(f"Overall: {p_success + g_success}/40")
    print("="*40)

if __name__ == "__main__":
    asyncio.run(main())
