import asyncio
import httpx
import time
import sys
import statistics

# Configuration
API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"

# Sample Questions for Load Testing
QUESTIONS = [
    "What is the price of milk?",
    "Show me deals for Coca-Cola.",
    "Best price for Ice Cream at Coles?",
    "Price of bread at Woolworths?",
    "How much is butter?",
    "Any deals on eggs?",
    "Price of bananas?",
    "Is there a discount on Tim Tam?",
    "Cheapest laundry detergent?",
    "Price of coffee pods?"
]

async def call_api(client, q, i, semaphore):
    async with semaphore:
        start_time = time.time()
        user_id = f"load_test_prod_{i}"
        try:
            response = await client.post(
                API_URL, 
                json={"text": q, "user_id": user_id}, 
                timeout=60.0
            )
            duration = time.time() - start_time
            if response.status_code == 200:
                print(f"Request {i+1}: ✅ Success in {duration:.2f}s")
                return True, duration
            else:
                print(f"Request {i+1}: ❌ Failed (HTTP {response.status_code}) in {duration:.2f}s")
                return False, duration
        except Exception as e:
            duration = time.time() - start_time
            print(f"Request {i+1}: ❌ Exception ({type(e).__name__}) in {duration:.2f}s")
            return False, duration

async def run_load_test(concurrency=5, total_requests=10):
    print(f"==========================================")
    print(f"🚀 LIVE LOAD TEST: {API_URL}")
    print(f"Concurrency: {concurrency} | Total Requests: {total_requests}")
    print(f"==========================================")
    
    semaphore = asyncio.Semaphore(concurrency)
    
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(total_requests):
            q = QUESTIONS[i % len(QUESTIONS)]
            tasks.append(call_api(client, q, i, semaphore))
            
        start_test = time.time()
        results = await asyncio.gather(*tasks)
        total_duration = time.time() - start_test
        
    successes = [d for s, d in results if s]
    failures = [d for s, d in results if not s]
    
    print(f"\n" + "="*40)
    print(f"📊 LOAD TEST SUMMARY")
    print(f"Total Requests: {total_requests}")
    print(f"Success Rate: {len(successes)}/{total_requests} ({len(successes)/total_requests*100:.1f}%)")
    print(f"Total Test Time: {total_duration:.2f}s")
    
    if successes:
        print(f"Avg Response Time: {statistics.mean(successes):.2f}s")
        print(f"Min Response Time: {min(successes):.2f}s")
        print(f"Max Response Time: {max(successes):.2f}s")
    print("="*40)

if __name__ == "__main__":
    concurrency = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    total_requests = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    asyncio.run(run_load_test(concurrency, total_requests))
