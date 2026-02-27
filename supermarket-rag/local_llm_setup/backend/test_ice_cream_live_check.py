import asyncio
import httpx
import json

API_URL = "https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"
# Exact query from user, including typo
QUERY = "pleaswe give me a ice cream price"

async def test_live():
    print(f"Testing Live API: {API_URL}")
    print(f"Query: '{QUERY}'")
    print("-" * 60)
    
    async with httpx.AsyncClient() as client:
        try:
            # Increased timeout for live API
            resp = await client.post(
                API_URL, 
                json={"text": QUERY, "user_id": "live_test_user"}, 
                timeout=120.0
            )
            
            if resp.status_code == 200:
                data = resp.json()
                print("\n[SUCCESS] Response received.")
                print("-" * 60)
                print("Response Text Snippet:")
                print(data.get("response", "")[:500] + "...\n")
                
                print("-" * 60)
                print("Metadata & Images:")
                meta = data.get("metadata", [])
                
                if not meta:
                    print("No metadata returned.")
                
                for idx, m in enumerate(meta):
                    img_url = m.get("image_url", "NO_URL")
                    score = m.get("score", "N/A")
                    shop = "Unknown Shop"
                    # Try to infer shop from file path/metadata
                    if "coles" in str(m).lower(): shop = "Coles"
                    elif "woolworths" in str(m).lower(): shop = "Woolworths"
                    
                    print(f"[{idx+1}] Shop: {shop} | Score: {score}")
                    print(f"    Image: {img_url}")
                    
                    # Check if URL is accessible
                    try:
                        img_resp = await client.head(img_url, timeout=5.0)
                        status = img_resp.status_code
                        print(f"    URL Status: {status}")
                    except Exception as e:
                        print(f"    URL Check Failed: {e}")
                        
            else:
                print(f"[ERROR] HTTP {resp.status_code}")
                print(resp.text)
                
        except Exception as e:
            print(f"[EXCEPTION] {e}")

if __name__ == "__main__":
    asyncio.run(test_live())
