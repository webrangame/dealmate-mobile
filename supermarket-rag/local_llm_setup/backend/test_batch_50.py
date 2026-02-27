import requests
import json
import time

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"
USER_ID = "test_user_123"

general_questions = [
    "Hello!",
    "Hi there, who are you?",
    "How can you help me today?",
    "Tell me a joke about shopping.",
    "What are some tips for saving money at the supermarket?",
    "How do I use this app?",
    "Thank you for your help.",
    "Goodbye.",
    "What is your name?",
    "Are you a robot?",
    "Can you give me a recipe for pasta?",
    "Is it better to shop in the morning or evening?",
    "What are common supermarket tricks to make me spend more?",
    "How do I check if an item is on sale?",
    "What shops do you compare?",
    "Who created you?",
    "What is the weather like? (testing fallback)",
    "Can you help me with my taxes? (testing boundaries)",
    "What is a RAG engine?",
    "How often do you update your prices?",
    "Do you have a mobile app?",
    "I'm looking for some deals, what should I do?",
    "Tell me about Coles.",
    "Tell me about Woolworths.",
    "Can you compare prices for me?"
]

product_questions = [
    "What is the price of full cream milk?",
    "How much does 1kg of sugar cost?",
    "Price of eggs at Coles?",
    "Is Coca-Cola on sale at Woolworths?",
    "Compare price of bread.",
    "What is the cheapest butter?",
    "How much is 500g of pasta?",
    "Price of bananas per kg?",
    "Do you have prices for laundry detergent?",
    "Cost of chicken breast?",
    "Is there a discount on chocolate?",
    "Price of 2L orange juice?",
    "How much are apples at Woolworths?",
    "Compare price of Pringles.",
    "What is the price of Berocca?",
    "How much is a 24 pack of water?",
    "Price of yogurt?",
    "Cost of olive oil?",
    "Is Nescafe on sale?",
    "How much is toilet paper?",
    "Price of breakfast cereal?",
    "Compare price of peanut butter.",
    "What is the cost of frozen peas?",
    "How much are snacks like chips?",
    "Price of shampoo?"
]

def run_tests():
    print(f"Starting tests on {API_URL}...")
    results = []

    def perform_query(q, category):
        print(f"Testing [{category}]: {q}")
        try:
            start_time = time.time()
            response = requests.post(API_URL, json={"text": q, "user_id": USER_ID}, timeout=30)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                resp_json = response.json()
                content = resp_json.get("response", "")
                # Simple check: RAG responses usually contain Markdown tables (| --- |)
                is_rag = "|---|" in content or "| --- |" in content
                results.append({
                    "question": q,
                    "category": category,
                    "status": "Success",
                    "is_rag_detected": is_rag,
                    "duration": f"{duration:.2f}s",
                    "preview": content[:100].replace('\n', ' ')
                })
            else:
                results.append({"question": q, "category": category, "status": f"Error {response.status_code}"})
        except Exception as e:
            results.append({"question": q, "category": category, "status": f"Exception: {str(e)}"})

    for q in general_questions:
        perform_query(q, "General")
        time.sleep(0.5) # Avoid hammering

    for q in product_questions:
        perform_query(q, "Product")
        time.sleep(0.5)

    # Save report
    with open("test_results_50.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nTest Complete. Summary:")
    general_success = len([r for r in results if r["category"] == "General" and r.get("status") == "Success"])
    product_success = len([r for r in results if r["category"] == "Product" and r.get("status") == "Success"])
    
    # Classification check
    # General should NOT be RAG. Product SHOULD be RAG (if found).
    general_non_rag = len([r for r in results if r["category"] == "General" and r.get("is_rag_detected") == False])
    product_rag = len([r for r in results if r["category"] == "Product" and r.get("is_rag_detected") == True])

    print(f"General: {general_success}/25 succeeded. Router accuracy: {general_non_rag}/25 used general response.")
    print(f"Product: {product_success}/25 succeeded. Router accuracy: {product_rag}/25 used RAG response.")

if __name__ == "__main__":
    run_tests()
