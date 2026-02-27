import os
import sys

# Try to load .env if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from llama_index.llms.litellm import LiteLLM

# Configuration from rag_engine.py
master_key = os.getenv("LITELLM_API_KEY", "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642")
litellm_api_base = os.getenv("LITELLM_API_BASE", "https://swzissb82u.us-east-1.awsapprunner.com")

print(f"LITELLM_API_BASE: {litellm_api_base}")

try:
    print("\n--- Testing LLM (openai/gemini-2.0-flash) ---")
    llm = LiteLLM(
        model="openai/gemini-2.0-flash", 
        api_key=master_key,
        api_base=litellm_api_base,
        temperature=0.1
    )
    print("LLM initialized.")
    response = llm.complete("Say 'LLM is working' if you can hear me.")
    print(f"LLM Response: {response}")
except Exception as e:
    print(f"LLM Test FAILED: {e}")
