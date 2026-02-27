import requests
import json
import sys

# API Endpoint (from earlier context or I can find it, but I'll use the service URL if I can find it, otherwise I'll assume it's the one I've been using)
# I need to find the Service URL. 
# Let me query it first.

def get_service_url():
    # Placeholder, will be replaced by actual logic in a separate command if needed, 
    # but for now I'll use a hardcoded one if I recall it or fetch it dynamically.
    # actually, better to fetch it dynamically in the script or pass it as an arg.
    # For now, let's assume I can get it via AWS CLI and pass it to this script, or just hardcode if I find it.
    # failed to find it in recent context? I can query it.
    pass

url = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"
# Actually, I should query it to be safe.

def test_fallback():
    query = "Nvidia RTX 5090" # Guaranteed missing from supermarket PDFs
    print(f"Testing fallback with query: {query}")
    
    try:
        response = requests.post(
            url,
            json={"text": query, "user_id": "test_script"},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        
        print("Response status:", response.status_code)
        print("Response body:")
        print(json.dumps(data, indent=2))
        
        answer = data.get("response", "")
        if "online results" in answer or "Web" in answer:
            print("\nSUCCESS: Fallback triggered and returned web results.")
        else:
            print("\nFAILURE: Fallback did not trigger or return web results.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    test_fallback()
