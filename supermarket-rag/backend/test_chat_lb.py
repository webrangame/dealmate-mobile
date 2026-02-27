import requests
import json
import sys

# Production URL
API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"

def test_chat(query="What is the price of milk?"):
    print(f"==========================================")
    print(f"Testing Chat via Load Balancer")
    print(f"URL: {API_URL}")
    print(f"Query: {query}")
    print(f"==========================================")
    
    payload = {
        "text": query,
        "user_id": "test_lb_user_69420"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Success! Response Received:")
            print("-" * 40)
            print(data.get("response", "No response text found."))
            print("-" * 40)
            
            metadata = data.get("metadata", [])
            if metadata:
                print(f"Sources: {len(metadata)} items found.")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return False

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "What is the price of milk?"
    test_chat(query)
