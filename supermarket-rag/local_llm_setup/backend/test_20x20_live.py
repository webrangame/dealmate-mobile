#!/usr/bin/env python3
"""
20x20 Live API Test Suite
Tests 20 general questions + 20 product questions against production API
"""
import asyncio
import httpx
import json
from datetime import datetime

# Production API endpoint
API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com"

# Test questions
GENERAL_QUESTIONS = [
    "What are the current specials at Coles?",
    "Do you have any half-price deals this week?",
    "What's on sale at Woolworths?",
    "Are there any discounts on meat?",
    "What chocolate is on special?",
    "Tell me about Valentine's Day deals",
    "What frozen treats are on sale?",
    "Are there any cat food promotions?",
    "What's the best deal on snacks?",
    "Any specials on breakfast items?",
    "What fruit and vegetables are on sale?",
    "Are there any buy 2 for $15 deals?",
    "What's on special in the dairy section?",
    "Any deals on cleaning products?",
    "What beverages are discounted?",
    "Are there any bakery specials?",
    "What's on sale for dinner tonight?",
    "Any health and beauty deals?",
    "What pet food is on special?",
    "Are there any online-only offers?"
]

PRODUCT_QUESTIONS = [
    "ice cream price",
    "milk price",
    "bread price",
    "chicken price",
    "beef price",
    "chocolate price",
    "coffee price",
    "tea price",
    "cheese price",
    "yogurt price",
    "apple price",
    "banana price",
    "tomato price",
    "potato price",
    "rice price",
    "pasta price",
    "cereal price",
    "eggs price",
    "butter price",
    "orange juice price"
]

async def test_question(client, question, question_type, index):
    """Test a single question"""
    try:
        response = await client.post(
            f"{API_URL}/chat",
            json={"text": question, "user_id": "test@example.com"},
            timeout=60.0
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for multi-shop coverage in product questions
            has_multi_shop = False
            if question_type == "product":
                response_text = data.get("response", "").lower()
                has_multi_shop = ("coles" in response_text and "woolworths" in response_text)
            
            return {
                "index": index,
                "type": question_type,
                "question": question,
                "status": "success",
                "response": data.get("response", "")[:200],  # First 200 chars
                "has_multi_shop": has_multi_shop,
                "response_time": response.elapsed.total_seconds()
            }
        else:
            return {
                "index": index,
                "type": question_type,
                "question": question,
                "status": "error",
                "error": f"HTTP {response.status_code}",
                "has_multi_shop": False
            }
    except Exception as e:
        return {
            "index": index,
            "type": question_type,
            "question": question,
            "status": "error",
            "error": str(e),
            "has_multi_shop": False
        }

async def run_tests():
    """Run all tests sequentially"""
    print("=" * 80)
    print("20x20 LIVE API TEST SUITE")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    
    async with httpx.AsyncClient() as client:
        # Test general questions
        print("Testing 20 General Questions...")
        print("-" * 80)
        for i, question in enumerate(GENERAL_QUESTIONS, 1):
            print(f"[{i}/20] {question}")
            result = await test_question(client, question, "general", i)
            results.append(result)
            status_icon = "✓" if result["status"] == "success" else "✗"
            print(f"    {status_icon} {result['status']}")
            await asyncio.sleep(1)  # Rate limiting
        
        print()
        print("Testing 20 Product Questions...")
        print("-" * 80)
        for i, question in enumerate(PRODUCT_QUESTIONS, 1):
            print(f"[{i}/20] {question}")
            result = await test_question(client, question, "product", i)
            results.append(result)
            status_icon = "✓" if result["status"] == "success" else "✗"
            multi_shop_icon = "🏪" if result.get("has_multi_shop") else ""
            print(f"    {status_icon} {result['status']} {multi_shop_icon}")
            await asyncio.sleep(1)  # Rate limiting
    
    # Calculate statistics
    total = len(results)
    successful = sum(1 for r in results if r["status"] == "success")
    general_success = sum(1 for r in results if r["type"] == "general" and r["status"] == "success")
    product_success = sum(1 for r in results if r["type"] == "product" and r["status"] == "success")
    multi_shop_count = sum(1 for r in results if r.get("has_multi_shop", False))
    
    # Save results
    output_file = "test_results_live_20x20.json"
    with open(output_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "api_url": API_URL,
            "summary": {
                "total_questions": total,
                "successful": successful,
                "failed": total - successful,
                "success_rate": f"{(successful/total)*100:.1f}%",
                "general_success": f"{general_success}/20",
                "product_success": f"{product_success}/20",
                "multi_shop_coverage": f"{multi_shop_count}/20 product questions"
            },
            "results": results
        }, f, indent=2)
    
    # Print summary
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Questions:        {total}")
    print(f"Successful:             {successful} ({(successful/total)*100:.1f}%)")
    print(f"Failed:                 {total - successful}")
    print(f"General Questions:      {general_success}/20")
    print(f"Product Questions:      {product_success}/20")
    print(f"Multi-Shop Coverage:    {multi_shop_count}/20 product questions ({(multi_shop_count/20)*100:.1f}%)")
    print()
    print(f"Results saved to: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_tests())
