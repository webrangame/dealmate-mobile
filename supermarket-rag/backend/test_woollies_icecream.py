import requests
import json
import uuid
import time

BASE_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com"
USER_ID = f"test_user_{uuid.uuid4().hex[:8]}"

def test_chat(message):
    url = f"{BASE_URL}/chat"
    payload = {
        "text": message, 
        "user_id": USER_ID
    }
    
    start = time.time()
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        duration = time.time() - start
        
        print(f"\nUser: {message}")
        print(f"Time: {duration:.2f}s")
        print(f"Assistant: {data.get('response', 'No response field')}")
        return data.get('response', "")
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response:
             print(f"Details: {e.response.text}")
        return ""

print(f"--- Checking Woolworths Vanilla Ice Cream ---")
resp = test_chat("Vanilla ice cream deals at Woolworths")
