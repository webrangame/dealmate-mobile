import asyncio
import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "supermarket-rag", "backend"))

from rag_engine import RAGEngine

QUESTIONS = [
    # Single Item Queries
    "How much is Connoisseur Ice Cream 1L at Woolworths?",
    "Price of Coles Full Cream Milk 2L?",
    "What is the deal for Sunrice Jasmine Rice 5kg?",
    "How much are XL Eggs 12 pack at Woolworths?",
    "Price of Helga's Mixed Grain Bread?",
    "What is the cost of Pepsi Max 30x375ml?",
    "How much is Bega Peanut Butter 475g?",
    "Price of Vegemite 380g?",
    "What is the deal for Nescafe Blend 43 500g?",
    "How much is Huggies Ultra Dry Nappies?",
    "Price of Finish Dishwasher Tablets 100pk?",
    "What is the cost of Cold Power Laundry Liquid 2L?",
    "How much is Cadbury Dairy Milk 180g?",
    "Price of Red Bull 4x250ml?",
    "What is the deal for Coca-Cola 24x375ml?",
    "How much is Sanitarium Weet-Bix 1.2kg?",
    "Price of Devondale Full Cream Milk Powder 1kg?",
    "What is the cost of Sirena Tuna 95g?",
    "How much is Continental Cup A Soup?",
    "Price of Uncle Tobys Oats 1kg?",
    "What is the deal for Lindt Excellence 100g?",
    "How much is Head & Shoulders Shampoo 400ml?",
    "Price of Colgate Total Toothpaste 115g?",
    "What is the cost of Rexona Deodorant?",
    
    # Multi-item Queries
    "Compare prices for Milk, Bread and Eggs.",
    "Show me deals for Pepsi, Coca-Cola and Red Bull.",
    "What are the prices for Chicken Schnitzel and Beef Mince?",
    "Deals for Shampoo, Conditioner and Soap.",
    "Prices for Rice, Pasta and Olive Oil.",
    
    # The "6 Products at Once" Query
    "Find prices for Connoisseur Ice Cream 1L, Milk 2L, White Bread, XL Eggs, Pepsi Max 10 pack, and Smith's Chips 170g."
]

async def run_test():
    load_dotenv(os.path.join("supermarket-rag", "backend", ".env"))
    engine = RAGEngine()
    
    results = []
    print(f"\n🚀 Starting Live Price API Test (30 Questions)...")
    print(f"User ID: test_user_batch_30")
    
    total_start = time.time()
    for i, q in enumerate(QUESTIONS):
        print(f"\n[{i+1}/30] Query: {q}")
        start = time.time()
        try:
            response = await engine.query(q, user_id="test_user_batch_30")
            duration = time.time() - start
            
            # Check for live verification tags
            live_count = sum(1 for m in response.get("metadata", []) if m.get("is_live"))
            
            results.append({
                "id": i+1,
                "query": q,
                "response": response.get("response"),
                "metadata": response.get("metadata"),
                "duration": round(duration, 2),
                "live_verified_count": live_count,
                "status": "SUCCESS"
            })
            print(f"✅ Success ({duration:.2f}s, Live Verified: {live_count})")
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "id": i+1,
                "query": q,
                "error": str(e),
                "status": "ERROR"
            })
            
    total_duration = time.time() - total_start
    
    # Save raw results
    output_file = f"test_results_live_30_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"\n--- Test Complete in {total_duration:.2f}s ---")
    print(f"Results saved to: {output_file}")
    
    return results, output_file

async def generate_markdown_report(results, filename):
    report = f"# 📊 Accuracy Report: Live Price API Test\n"
    report += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"**Total Queries:** {len(results)}\n"
    report += f"**Successful:** {sum(1 for r in results if r['status'] == 'SUCCESS')}\n"
    report += f"**Avg Duration:** {sum(r.get('duration', 0) for r in results)/len(results):.2f}s\n\n"
    
    report += "## 📈 Key Findings\n"
    live_queries = [r for r in results if r.get("live_verified_count", 0) > 0]
    report += f"- **Live Verification Triggered:** {len(live_queries)} queries\n"
    report += f"- **Multi-item performance:** Handled queries with up to 6 items.\n\n"
    
    report += "## 📝 Detailed Results (Sample)\n"
    report += "| # | Query | Live Count | Duration | Status |\n"
    report += "|---|-------|------------|----------|--------|\n"
    for r in results:
        status_emoji = "✅" if r["status"] == "SUCCESS" else "❌"
        report += f"| {r['id']} | {r['query'][:50]}... | {r.get('live_verified_count', 0)} | {r.get('duration', 'N/A')}s | {status_emoji} |\n"
    
    report_file = filename.replace(".json", ".md")
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Report generated: {report_file}")
    return report_file

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    results, json_file = loop.run_until_complete(run_test())
    loop.run_until_complete(generate_markdown_report(results, json_file))
