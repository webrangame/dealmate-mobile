import asyncio
import os
import json
import time
from dotenv import load_dotenv
from rag_engine import RAGEngine

async def run_mass_tests():
    load_dotenv()
    engine = RAGEngine()
    
    reports = {}

    # Scenario 1: 5 products in 1 query
    print("\n--- TEST 1: 5 products ---")
    query_5 = "price of milk, bread, eggs, butter and rice"
    start_5 = time.time()
    resp_5 = await engine.query(query_5, user_id="mass_test_5")
    reports["test_5_items"] = {
        "query": query_5,
        "duration": round(time.time() - start_5, 2),
        "metadata_count": len(resp_5.get("metadata", [])),
        "response_preview": resp_5.get("response")[:200] + "..."
    }

    # Scenario 2: 10 products in 1 query
    print("\n--- TEST 2: 10 products ---")
    query_10 = "i need prices for coca cola, pepsi, chips, chocolate, coffee, tea, sugar, flour, salt and oil"
    start_10 = time.time()
    resp_10 = await engine.query(query_10, user_id="mass_test_10")
    reports["test_10_items"] = {
        "query": query_10,
        "duration": round(time.time() - start_10, 2),
        "metadata_count": len(resp_10.get("metadata", [])),
        "response_preview": resp_10.get("response")[:200] + "..."
    }

    # Scenario 3: 20 single products
    print("\n--- TEST 3: 20 single products ---")
    single_items = [
        "milk", "bread", "eggs", "butter", "rice", 
        "coke", "chips", "pasta", "cheese", "apples",
        "bananas", "chicken", "beef", "yogurt", "cereal",
        "coffee", "tea", "detergent", "shampoo", "soap"
    ]
    single_results = []
    total_start = time.time()
    for item in single_items:
        q = f"price of {item}"
        print(f"Testing single: {q}")
        start = time.time()
        resp = await engine.query(q, user_id="mass_test_20")
        single_results.append({
            "item": item,
            "duration": round(time.time() - start, 2),
            "found": len(resp.get("metadata", [])) > 0
        })
    
    reports["test_20_single"] = {
        "total_duration": round(time.time() - total_start, 2),
        "items": single_results,
        "success_rate": f"{sum(1 for r in single_results if r['found'])}/20"
    }

    with open("mass_test_results.json", "w") as f:
        json.dump(reports, f, indent=2)
    
    print("\nMass testing completed. Results saved to mass_test_results.json")

if __name__ == "__main__":
    asyncio.run(run_mass_tests())
