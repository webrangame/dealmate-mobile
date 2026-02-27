import httpx
import json
import asyncio
import time

async def test_streaming():
    url = "http://localhost:8000/chat"
    payload = {
        "text": "compare prices for Cadbury and Red Bull",
        "user_id": "test_user_local",
        "stream": True
    }
    
    print(f"Sending multi-product streaming request to {url}...")
    start_time = time.time()
    first_chunk_time = None
    
    async with httpx.AsyncClient(timeout=180.0) as client:
        async with client.stream("POST", url, json=payload) as response:
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                # print(await response.aread())
                return

            print("\n--- STREAM START ---")
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                
                try:
                    data = json.loads(line)
                    if not first_chunk_time:
                        first_chunk_time = time.time()
                        print(f"\n[First chunk received after {first_chunk_time - start_time:.2f}s]")
                    
                    if data["type"] == "chunk":
                        print(data["content"], end="", flush=True)
                    elif data["type"] == "done":
                        print("\n\n--- STREAM DONE ---")
                        print(f"Final Response Length: {len(data['response'])}")
                        print(f"Metadata Count: {len(data['metadata'])}")
                        if data['metadata']:
                            print("\nTop Products Found:")
                            for m in data['metadata'][:4]:
                                print(f"- {m['store']}: {m['product']} ({m['price']})")
                except Exception as e:
                    print(f"\nParse Error: {e} | Line: {line}")
    
    end_time = time.time()
    print(f"\nTotal time: {end_time - start_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(test_streaming())
