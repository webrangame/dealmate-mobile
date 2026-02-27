
import requests
import json
import time

API_URL = "http://127.0.0.1:8001/chat"

questions = [
    "product: Price of Milk",
    "product: Cola 2L"
]

def test_question(question):
    payload = {
        "text": question,
        "user_id": "test_user"
    }
    
    start_time = time.time()
    try:
        print(f"Testing: {question}")
        response = requests.post(API_URL, json=payload, timeout=120)
        end_time = time.time()
        latency = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "")
            print(f"  -> {latency:.2f}s | Success")
            print(f"  Answer: {answer[:200]}...")
            return True
        else:
            print(f"  -> {latency:.2f}s | Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  -> Error: {str(e)}")
        return False

if __name__ == "__main__":
    print(f"🚀 Starting Test (2 Questions) on {API_URL}...")
    for q in questions:
        test_question(q)
