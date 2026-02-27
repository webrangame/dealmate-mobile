import requests
import time
import json
import random

API_URL = "http://localhost:8001/chat"

questions = [
    "what is the price of ice cream",
    "how much are bananas?"
]

def benchmark():
    print(f"Starting benchmark with {len(questions)} questions...")
    print("-" * 50)
    
    success_count = 0
    total_time = 0
    
    for i, q in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] Asking: '{q}'", end=" ", flush=True)
        start = time.time()
        try:
            response = requests.post(API_URL, json={"text": q}, timeout=300)
            duration = time.time() - start
            total_time += duration
            
            if response.status_code == 200:
                print(f"✅ ({duration:.2f}s) - {response.json().get('response')}")
                success_count += 1
            else:
                print(f"❌ ({duration:.2f}s) - HTTP {response.status_code}: {response.text}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            
    print("-" * 50)
    print(f"Benchmark Complete. Success Rate: {success_count}/{len(questions)}")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Avg Latency: {(total_time/len(questions)):.2f}s")

if __name__ == "__main__":
    benchmark()
