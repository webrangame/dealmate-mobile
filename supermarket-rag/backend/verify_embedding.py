import os
import sys

# Try to load .env if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from llama_index.core import Settings
from llama_index.embeddings.litellm import LiteLLMEmbedding
import litellm

# Configuration from rag_engine.py
master_key = os.getenv("LITELLM_API_KEY")
litellm_api_base = os.getenv("LITELLM_API_BASE", "https://swzissb82u.us-east-1.awsapprunner.com")

if not master_key:
    # Fallback for manual test
    master_key = "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
    
print(f"LITELLM_API_BASE: {litellm_api_base}")

# Fix for Gemini embedding: Drop unsupported params like encoding_format
litellm.drop_params = True

# Test Embedding
try:
    print("\n--- Testing Embedding (BAAI/bge-small-en-v1.5) ---")
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )
    print("Embedding model initialized.")
    # Simple embedding test
    text = "This is a test sentence."
    embedding = Settings.embed_model.get_text_embedding(text)
    print(f"SUCCESS! Embedding generated. Vector length: {len(embedding)}")
    print(f"First 5 dimensions: {embedding[:5]}")
except Exception as e:
    print(f"Embedding Test FAILED: {e}")
    import traceback
    traceback.print_exc()
