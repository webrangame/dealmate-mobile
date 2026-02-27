#!/usr/bin/env python3
"""
Live API Testing Script
Tests the supermarket RAG API with product and general questions
"""
import httpx
import asyncio
import json
from datetime import datetime

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"
USER_ID = "test_user_verification"

# 20 Product-related questions (ice cream and other products)
PRODUCT_QUESTIONS = [
    "What is the price of ice cream at Coles?",
    "How much does ice cream cost at Woolworths?",
    "Which store has cheaper ice cream, Coles or Woolworths?",
    "What ice cream brands are on sale this week?",
    "Show me all ice cream deals",
    "What's the cheapest ice cream available?",
    "Are there any ice cream specials at Coles?",
    "Compare ice cream prices between Coles and Woolworths",
    "What flavors of ice cream are discounted?",
    "How much is Ben & Jerry's ice cream?",
    "What's the price of Connoisseur ice cream?",
    "Are there any 2 for 1 ice cream deals?",
    "What size ice cream tubs are on special?",
    "Show me premium ice cream prices",
    "What's the price difference for ice cream between stores?",
    "Are there any ice cream promotions this week?",
    "What's the regular price vs sale price for ice cream?",
    "Which store has the best ice cream value?",
    "What ice cream products are under $5?",
    "Compare Magnum ice cream prices at both stores"
]

# 20 General questions (testing RAG capabilities)
GENERAL_QUESTIONS = [
    "What products are on sale this week?",
    "Which store is cheaper overall?",
    "What are the best deals at Coles?",
    "Show me Woolworths specials",
    "What's the price of milk?",
    "Compare bread prices",
    "What fruits are on sale?",
    "Are there any meat specials?",
    "What's the cheapest way to buy vegetables?",
    "Show me all dairy products on sale",
    "What snacks are discounted this week?",
    "Compare chicken prices between stores",
    "What beverages are on special?",
    "Are there any breakfast cereal deals?",
    "What's the price of eggs?",
    "Show me cleaning product specials",
    "What pasta is on sale?",
    "Compare rice prices",
    "What frozen food deals are available?",
    "Are there any buy one get one free offers?"
]

async def test_query(client, question, question_type, index):
    """Test a single query and return results"""
    try:
        response = await client.post(
            API_URL,
            json={"text": question, "user_id": USER_ID},
            timeout=30.0
        )
        
        result = {
            "index": index,
            "type": question_type,
            "question": question,
            "status_code": response.status_code,
            "success": response.status_code == 200,
            "response_time": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else 0,
        }
        
        if response.status_code == 200:
            data = response.json()
            result["response"] = data.get("response", "")
            result["response_length"] = len(data.get("response", ""))
        else:
            result["error"] = response.text
            
        return result
        
    except Exception as e:
        return {
            "index": index,
            "type": question_type,
            "question": question,
            "status_code": 0,
            "success": False,
            "error": str(e)
        }

async def run_tests():
    """Run all test queries"""
    print("=" * 80)
    print("LIVE API TESTING - Supermarket RAG")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Endpoint: {API_URL}")
    print(f"Total Questions: {len(PRODUCT_QUESTIONS) + len(GENERAL_QUESTIONS)}")
    print("=" * 80)
    
    results = []
    
    async with httpx.AsyncClient() as client:
        # Test product questions
        print("\n📦 Testing Product Questions (Ice Cream)...")
        for i, question in enumerate(PRODUCT_QUESTIONS, 1):
            print(f"  [{i}/20] {question[:60]}...")
            result = await test_query(client, question, "product", i)
            results.append(result)
            if result["success"]:
                print(f"      ✅ Success ({result.get('response_length', 0)} chars)")
            else:
                print(f"      ❌ Failed: {result.get('error', 'Unknown error')}")
            await asyncio.sleep(0.5)  # Rate limiting
        
        # Test general questions
        print("\n🔍 Testing General Questions...")
        for i, question in enumerate(GENERAL_QUESTIONS, 1):
            print(f"  [{i}/20] {question[:60]}...")
            result = await test_query(client, question, "general", i)
            results.append(result)
            if result["success"]:
                print(f"      ✅ Success ({result.get('response_length', 0)} chars)")
            else:
                print(f"      ❌ Failed: {result.get('error', 'Unknown error')}")
            await asyncio.sleep(0.5)  # Rate limiting
    
    # Generate report
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    failed = total - successful
    
    product_results = [r for r in results if r["type"] == "product"]
    general_results = [r for r in results if r["type"] == "general"]
    
    product_success = sum(1 for r in product_results if r["success"])
    general_success = sum(1 for r in general_results if r["success"])
    
    print(f"\n📊 Overall Statistics:")
    print(f"  Total Queries: {total}")
    print(f"  ✅ Successful: {successful} ({successful/total*100:.1f}%)")
    print(f"  ❌ Failed: {failed} ({failed/total*100:.1f}%)")
    
    print(f"\n📦 Product Questions (Ice Cream):")
    print(f"  Success Rate: {product_success}/20 ({product_success/20*100:.1f}%)")
    
    print(f"\n🔍 General Questions:")
    print(f"  Success Rate: {general_success}/20 ({general_success/20*100:.1f}%)")
    
    # Identify issues
    print(f"\n🔍 Issue Analysis:")
    if failed > 0:
        print(f"  ⚠️ Found {failed} failed queries:")
        for r in results:
            if not r["success"]:
                print(f"    - Q{r['index']}: {r['question'][:50]}...")
                print(f"      Error: {r.get('error', 'Unknown')}")
    else:
        print(f"  ✅ No failures detected!")
    
    # Check response quality
    empty_responses = sum(1 for r in results if r["success"] and r.get("response_length", 0) < 50)
    if empty_responses > 0:
        print(f"\n  ⚠️ Warning: {empty_responses} queries returned very short responses (< 50 chars)")
    
    # Save detailed report
    report_file = f"/tmp/api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "successful": successful,
                "failed": failed,
                "product_success_rate": f"{product_success/20*100:.1f}%",
                "general_success_rate": f"{general_success/20*100:.1f}%"
            },
            "results": results
        }, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    print("=" * 80)
    
    return results, successful == total

if __name__ == "__main__":
    results, all_passed = asyncio.run(run_tests())
    exit(0 if all_passed else 1)
