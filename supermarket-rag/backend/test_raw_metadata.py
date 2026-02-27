import asyncio
import json
import os
from rag_engine import RAGEngine

async def test_ice_cream_metadata():
    engine = RAGEngine()
    query_text = "i need to eat ice cream today"
    user_id = "test_image_raw"
    
    user_key = await engine._ensure_user_key(user_id)
    from llama_index.llms.litellm import LiteLLM
    from llama_index.core import Settings
    user_llm = LiteLLM(model="openai/gemini-2.0-flash", api_key=user_key, api_base=engine.litellm_api_base, temperature=0.1)
    user_embed_model = Settings.embed_model
    
    # Do keyword search directly to bypass RAG layers and see what data exists
    brand_keywords = []
    keywords = ["ice", "cream"]
    noise_keywords = []
    
    top_candidates = await engine._hybrid_search("i need to eat ice cream today", {"product": "ice cream", "category": "Dairy"}, brand_keywords, keywords, noise_keywords, user_embed_model)
    
    print("\n--- Raw DB Candidates Metadata ---")
    for i, n in enumerate(top_candidates[:15]):
        m = n.node.metadata
        print(f"\n[{i}] Shop: {m.get('shop_name')}")
        print(f"    Page IMG: {m.get('page_image_url')}")
        print(f"    Product Name: {m.get('product_name')}")
        print(f"    Item Name: {m.get('item_name')}")
        print(f"    Text: {n.node.text[:100]}...")

if __name__ == "__main__":
    asyncio.run(test_ice_cream_metadata())
