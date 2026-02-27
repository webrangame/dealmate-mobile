import requests
import json
import time
from datetime import datetime

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"

# Comprehensive test suite - 50 queries total
TEST_QUERIES = {
    "General Products (20)": [
        "ice cream price",
        "chips price", 
        "chocolate price",
        "milk price",
        "bread price",
        "butter price",
        "cheese price",
        "yogurt price",
        "biscuits price",
        "pasta price",
        "rice price",
        "coffee price",
        "tea price",
        "sugar price",
        "flour price",
        "eggs price",
        "chicken price",
        "beef price",
        "bacon price",
        "soft drink price"
    ],
    "Specific Products (20)": [
        "Bulla ice cream",
        "Peters ice cream",
        "Coca Cola",
        "Pepsi",
        "Oreo",
        "Drumstix crackers",
        "Tim Tams",
        "Arnott's Shapes",
        "Cadbury chocolate",
        "Nestle chocolate",
        "Pringles chips",
        "Smith's chips",
        "Barilla pasta",
        "SunRice",
        "Nescafe coffee",
        "Lipton tea",
        "CSR sugar",
        "White Wings flour",
        "Dairy Farmers milk",
        "Bega cheese"
    ],
    "General Questions (10)": [
        "what's the cheapest ice cream?",
        "which shop has better chocolate deals?",
        "show me soft drink prices",
        "compare biscuit prices",
        "where can I find cheap milk?",
        "best coffee deals",
        "cheapest pasta options",
        "which shop has better chip prices?",
        "compare yogurt prices",
        "best snack deals"
    ]
}

def test_query(query):
    """Test a single query and return detailed results"""
    try:
        response = requests.post(
            API_URL,
            json={"text": query, "user_id": "comprehensive_test"},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        
        response_text = data.get("response", "")
        metadata = data.get("metadata", [])
        
        # Count shop results
        shops = set()
        for m in metadata:
            shop = m.get("shop_name")
            if shop:
                shops.add(shop)
        
        # Check for both shops in response TEXT (most important)
        has_coles_text = "coles" in response_text.lower()
        has_woolworths_text = "woolworths" in response_text.lower()
        
        # Also check metadata
        has_coles_meta = "Coles" in shops
        has_woolworths_meta = "Woolworths" in shops
        
        # Combined check
        has_coles = has_coles_text or has_coles_meta
        has_woolworths = has_woolworths_text or has_woolworths_meta
        
        return {
            "success": True,
            "query": query,
            "has_coles": has_coles,
            "has_woolworths": has_woolworths,
            "both_shops": has_coles and has_woolworths,
            "num_images": len(metadata),
            "shops_found": list(shops),
            "response_length": len(response_text),
            "response_preview": response_text[:300] + "..." if len(response_text) > 300 else response_text
        }
        
    except Exception as e:
        return {
            "success": False,
            "query": query,
            "error": str(e)
        }

def generate_comprehensive_report():
    """Run all 50 tests and generate detailed report"""
    print("=" * 80)
    print(f"COMPREHENSIVE API VERIFICATION - 50 QUERIES")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Endpoint: {API_URL}")
    print("=" * 80)
    
    all_results = []
    total_queries = sum(len(queries) for queries in TEST_QUERIES.values())
    current = 0
    
    for category, queries in TEST_QUERIES.items():
        print(f"\n\n{'='*80}")
        print(f"TESTING: {category}")
        print('='*80)
        
        category_results = []
        
        for query in queries:
            current += 1
            print(f"\n[{current}/{total_queries}] Query: '{query}'")
            print("-" * 60)
            
            result = test_query(query)
            category_results.append(result)
            
            if result["success"]:
                both_icon = "✅" if result['both_shops'] else "⚠️"
                print(f"{both_icon} Coles: {'✓' if result['has_coles'] else '✗'} | "
                      f"Woolworths: {'✓' if result['has_woolworths'] else '✗'} | "
                      f"Images: {result['num_images']}")
            else:
                print(f"❌ Failed: {result['error']}")
            
            time.sleep(0.5)  # Rate limiting
        
        all_results.append({
            "category": category,
            "results": category_results
        })
    
    # Detailed summary statistics
    print("\n\n" + "=" * 80)
    print("COMPREHENSIVE SUMMARY")
    print("=" * 80)
    
    total_tests = sum(len(cat["results"]) for cat in all_results)
    successful_tests = sum(1 for cat in all_results for r in cat["results"] if r["success"])
    both_shops_count = sum(1 for cat in all_results for r in cat["results"] if r.get("both_shops", False))
    
    print(f"\nOverall Results:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Successful: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
    print(f"  Both Shops: {both_shops_count}/{successful_tests} ({both_shops_count/successful_tests*100:.1f}%)")
    
    # Category breakdown
    print(f"\nBy Category:")
    for cat in all_results:
        cat_results = cat["results"]
        cat_success = sum(1 for r in cat_results if r["success"])
        cat_both = sum(1 for r in cat_results if r.get("both_shops", False))
        cat_pct = (cat_both/cat_success*100) if cat_success > 0 else 0
        print(f"  {cat['category']}: {cat_both}/{cat_success} ({cat_pct:.1f}%)")
    
    # Issues
    print("\n\nQUERIES MISSING ONE OR BOTH SHOPS:")
    issues = []
    for cat in all_results:
        for r in cat["results"]:
            if r["success"] and not r.get("both_shops"):
                issues.append(r)
                shops_str = ', '.join(r['shops_found']) if r['shops_found'] else 'None'
                print(f"  ⚠️  '{r['query']}' - Only: {shops_str}")
    
    if not issues:
        print("  ✅ None - All queries returned both shops!")
    
    # Improvement metrics
    print(f"\n\nIMPROVEMENT METRICS:")
    print(f"  Previous (before fixes): 28.6% both shops (4/14)")
    print(f"  Current (after fixes): {both_shops_count/successful_tests*100:.1f}% both shops ({both_shops_count}/{successful_tests})")
    improvement = (both_shops_count/successful_tests*100) - 28.6
    print(f"  Improvement: {improvement:+.1f} percentage points")
    
    # Save detailed JSON report
    with open("comprehensive_test_results.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "endpoint": API_URL,
            "summary": {
                "total_tests": total_tests,
                "successful": successful_tests,
                "both_shops_count": both_shops_count,
                "both_shops_percentage": both_shops_count/successful_tests*100 if successful_tests > 0 else 0
            },
            "results": all_results
        }, f, indent=2)
    
    print(f"\n\nDetailed JSON report: comprehensive_test_results.json")
    print("=" * 80)

if __name__ == "__main__":
    generate_comprehensive_report()
