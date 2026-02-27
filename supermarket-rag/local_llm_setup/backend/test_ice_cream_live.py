import requests
import json

url = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"

payload = {
    "text": "ice cream price",
    "user_id": "test_debug"
}

print("Testing live API with query: 'ice cream price'")
print("=" * 60)

try:
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    
    data = response.json()
    
    print("\n=== RESPONSE ===")
    print(data.get("response", ""))
    
    print("\n\n=== METADATA (Images) ===")
    metadata = data.get("metadata", [])
    print(f"Found {len(metadata)} images")
    for m in metadata:
        print(f"- {m.get('shop_name')}: Page {m.get('page')}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
