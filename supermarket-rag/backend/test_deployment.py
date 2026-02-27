import requests
import json
import time
from datetime import datetime

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"

# Test categories
TEST_QUERIES = {
    "Common Products": [
        "ice cream price",
        "chips price",
        "chocolate price",
        "milk price",
        "bread price"
    ],
    "Specific Products": [
        "Bulla ice cream",
        "Peters ice cream",
        "Coca Cola",
        "Oreo",
        "Drumstix crackers"
    ],
    "General Questions": [
        "what's the cheapest ice cream?",
        "which shop has better chocolate deals?",
        "show me soft drink prices",
        "compare biscuit prices"
    ]
}

def test_query(query):
    """Test a single query and return results"""
    try:
        response = requests.post(
            API_URL,
            json={"text": query, "user_id": "test_verification"},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        
        # Analyze response
        response_text = data.get("response", "")
        metadata = data.get("metadata", [])
        
        # Count shop results
        shops = set()
        for m in metadata:
            shop = m.get("shop_name")
            if shop:
                shops.add(shop)
        
        # Check for both shops
        has_coles = "coles" in response_text.lower() or "Coles" in shops
        has_woolworths = "woolworths" in response_text.lower() or "Woolworths" in shops
        
        return {
            "success": True,
            "query": query,
            "has_coles": has_coles,
            "has_woolworths": has_woolworths,
            "both_shops": has_coles and has_woolworths,
            "num_images": len(metadata),
            "shops_found": list(shops),
            "response_length": len(response_text),
            "response_preview": response_text[:200] + "..." if len(response_text) > 200 else response_text
        }
        
    except Exception as e:
        return {
            "success": False,
            "query": query,
            "error": str(e)
        }

def generate_report():
    """Run all tests and generate report"""
    print("=" * 80)
    print(f"API VERIFICATION REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Endpoint: {API_URL}")
    print("=" * 80)
    
    all_results = []
    
    for category, queries in TEST_QUERIES.items():
        print(f"\n\n{'='*80}")
        print(f"TESTING: {category}")
        print('='*80)
        
        category_results = []
        
        for query in queries:
            print(f"\nQuery: '{query}'")
            print("-" * 60)
            
            result = test_query(query)
            category_results.append(result)
            
            if result["success"]:
                print(f"✅ Success")
                print(f"   Coles: {'✓' if result['has_coles'] else '✗'}")
                print(f"   Woolworths: {'✓' if result['has_woolworths'] else '✗'}")
                print(f"   Both shops: {'✓' if result['both_shops'] else '✗'}")
                print(f"   Images: {result['num_images']}")
                print(f"   Preview: {result['response_preview']}")
            else:
                print(f"❌ Failed: {result['error']}")
            
            time.sleep(1)  # Rate limiting
        
        all_results.append({
            "category": category,
            "results": category_results
        })
    
    # Summary statistics
    print("\n\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    total_tests = sum(len(cat["results"]) for cat in all_results)
    successful_tests = sum(1 for cat in all_results for r in cat["results"] if r["success"])
    both_shops_count = sum(1 for cat in all_results for r in cat["results"] if r.get("both_shops", False))
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
    print(f"Both Shops Returned: {both_shops_count}/{successful_tests} ({both_shops_count/successful_tests*100:.1f}% if successful_tests > 0 else 0)")
    
    # Critical issues
    print("\n\nCRITICAL ISSUES:")
    issues_found = False
    for cat in all_results:
        for r in cat["results"]:
            if r["success"] and not r.get("both_shops"):
                if not issues_found:
                    print("")
                issues_found = True
                print(f"⚠️  '{r['query']}' - Only returned: {', '.join(r['shops_found'])}")
    
    if not issues_found:
        print("✅ None - All queries returned results from both shops!")
    
    # Save detailed JSON report
    with open("verification_report.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "endpoint": API_URL,
            "summary": {
                "total_tests": total_tests,
                "successful": successful_tests,
                "both_shops_count": both_shops_count
            },
            "results": all_results
        }, f, indent=2)
    
    print(f"\n\nDetailed report saved to: verification_report.json")
    print("=" * 80)

if __name__ == "__main__":
    generate_report()
