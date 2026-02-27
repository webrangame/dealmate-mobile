import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

async def verify_history():
    load_dotenv()
    # Test on local server
    base_url = "http://localhost:8000"
    user_id = "test_user_6789"
    session_id = "test_session_123"
    
    print(f"--- 1. Sending a message with session_id {session_id} ---")
    chat_url = f"{base_url}/chat"
    payload = {
        "text": "what is the price of milk?",
        "user_id": user_id,
        "session_id": session_id,
        "stream": False
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(chat_url, json=payload)
            print(f"Chat Response Status: {resp.status_code}")
            if resp.status_code == 200:
                print("Message sent successfully and logged.")
            else:
                print(f"Error: {resp.text}")
        except Exception as e:
            print(f"Request failed: {e}")

    print(f"\n--- 2. Fetching conversation list for user {user_id} ---")
    history_url = f"{base_url}/chat/history?user_id={user_id}"
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(history_url)
            print(f"History Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                conversations = data.get("conversations", [])
                print(f"Found {len(conversations)} conversations.")
                for conv in conversations:
                    print(f" - Session: {conv['session_id']}, Title: {conv['title']}")
            else:
                print(f"Error: {resp.text}")
        except Exception as e:
            print(f"Request failed: {e}")

    print(f"\n--- 3. Fetching messages for session {session_id} ---")
    messages_url = f"{base_url}/chat/history/{session_id}?user_id={user_id}"
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(messages_url)
            print(f"Messages Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                messages = data.get("messages", [])
                print(f"Found {len(messages)} messages.")
                for i, msg in enumerate(messages):
                    print(f" [{msg['role']}]: {msg['content'][:50]}...")
            else:
                print(f"Error: {resp.text}")
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify_history())
