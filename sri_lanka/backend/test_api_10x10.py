import asyncio
import httpx
import json
import time
from datetime import datetime

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"
USER_ID = "test_user@gmail.com"

# 10 General Questions
GENERAL_QUESTIONS = [
    "Hello",
    "Good morning",
    "Who are you?",
    "What can you do?",
    "How does this app work?",
    "Thanks",
    "What is the weather today?",
    "Tell me a joke",
    "What time is it?",
    "Goodbye"
]

# 10 Product Questions
PRODUCT_QUESTIONS = [
    "Price of milk",
    "How much is Coca Cola?",
    "Cheapest bread",
    "Cost of bananas",
    "Price of eggs",
    "Woolworths pasta sauce",
    "Cadbury chocolate",
    "Price of Tim Tams",
    "Frozen chips price",
    "Toilet paper price"
]

async def test_question(client, question, question_num, question_type):
    """Test a single question"""
    print(f"\n{'='*60}")
    print(f"[{question_num}] {question_type} Question: {question}")
    print('='*60)
    
    start_time = time.time()
    try:
        response = await client.post(API_URL, json={"text": question, "user_id": USER_ID})
        duration = time.time() - start_time
        
        result = {
            "question_num": question_num,
            "type": question_type,
            "question": question,
            "status_code": response.status_code,
            "duration": round(duration, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        if response.status_code == 200:
            resp_json = response.json()
            result["response"] = resp_json
            print(f"✅ SUCCESS ({duration:.2f}s)")
            print(f"Response: {resp_json.get('response', resp_json)}")
        else:
            result["error"] = response.text
            print(f"❌ ERROR {response.status_code} ({duration:.2f}s)")
            print(f"Error: {response.text}")
            
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ EXCEPTION ({duration:.2f}s): {e}")
        return {
            "question_num": question_num,
            "type": question_type,
            "question": question,
            "status_code": 0,
            "error": str(e),
            "duration": round(duration, 2),
            "timestamp": datetime.now().isoformat()
        }

async def run_tests():
    """Run all tests"""
    results = []
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║         SUPERMARKET RAG API TEST - 10 + 10                 ║
╚════════════════════════════════════════════════════════════╝
API: {API_URL}
User: {USER_ID}
Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test General Questions
        print("\n" + "█"*60)
        print("TESTING GENERAL QUESTIONS (10)")
        print("█"*60)
        
        for i, question in enumerate(GENERAL_QUESTIONS):
            result = await test_question(client, question, i+1, "General")
            results.append(result)
            if i < len(GENERAL_QUESTIONS) - 1:
                await asyncio.sleep(3)  # Rate limit
        
        # Test Product Questions  
        print("\n\n" + "█"*60)
        print("TESTING PRODUCT QUESTIONS (10)")
        print("█"*60)
        
        for i, question in enumerate(PRODUCT_QUESTIONS):
            result = await test_question(client, question, i+11, "Product")
            results.append(result)
            if i < len(PRODUCT_QUESTIONS) - 1:
                await asyncio.sleep(3)  # Rate limit
    
    # Save Results
    filename = "test_api_10x10_results.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    # Generate Summary
    print("\n\n" + "╔"+"═"*58+"╗")
    print("║" + " "*20 + "TEST SUMMARY" + " "*26 + "║")
    print("╚"+"═"*58+"╝")
    
    total_tests = len(results)
    successful = sum(1 for r in results if r["status_code"] == 200)
    failed = total_tests - successful
    
    general_success = sum(1 for r in results if r["type"] == "General" and r["status_code"] == 200)
    product_success = sum(1 for r in results if r["type"] == "Product" and r["status_code"] == 200)
    
    avg_duration = sum(r["duration"] for r in results) / len(results)
    
    print(f"\n📊 Overall Results:")
    print(f"   Total Tests:     {total_tests}")
    print(f"   ✅ Successful:   {successful}")
    print(f"   ❌ Failed:       {failed}")
    print(f"   Success Rate:    {(successful/total_tests)*100:.1f}%")
    
    print(f"\n📋 By Type:")
    print(f"   General Q:       {general_success}/10 ({(general_success/10)*100:.0f}%)")
    print(f"   Product Q:       {product_success}/10 ({(product_success/10)*100:.0f}%)")
    
    print(f"\n⏱️  Performance:")
    print(f"   Avg Duration:    {avg_duration:.2f}s")
    
    print(f"\n💾 Results saved to: {filename}")
    print(f"🕒 End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    asyncio.run(run_tests())
