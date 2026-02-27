from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import time

print("Initializing HuggingFaceEmbedding (BAAI/bge-small-en-v1.5)...")
start_time = time.time()
try:
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    print(f"Model loaded in {time.time() - start_time:.2f}s")

    text = "Supermarket catalogue specials for Coles and Woolworths"
    print(f"Generating embedding for: '{text}'")
    embedding = embed_model.get_text_embedding(text)
    
    print(f"SUCCESS! Embedding length: {len(embedding)}")
    print(f"First 5 dimensions: {embedding[:5]}")
except Exception as e:
    print(f"FAILED: {e}")
