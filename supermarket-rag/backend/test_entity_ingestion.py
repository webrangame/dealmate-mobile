
import asyncio
from rag_engine import RAGEngine
import os
import json

async def test_ingestion():
    print("=== Testing Entity-Level Ingestion ===")
    engine = RAGEngine()
    
    # We need a PDF to test. Let's look for one in the upload folder.
    data_dir = "uploaded_docs"
    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} does not exist.")
        return

    pdfs = [f for f in os.listdir(data_dir) if f.endswith(".pdf")]
    if not pdfs:
        print("No PDFs found in 'backend/data/'. Please add one to test.")
        return
    
    # Ingest pages 0, 1, 2 from both PDFs
    page_indices = {
        "Woolworths.pdf": [0, 1, 2],
        "Coles.pdf": [0, 1, 2]
    }
    
    total_count = 0
    for pdf in ["Woolworths.pdf", "Coles.pdf"]:
        print(f"\n--- Ingesting {pdf} (Pages 0-2) ---")
        count = await engine.ingest_documents(data_dir, specific_file=pdf, page_indices={pdf: [0, 1, 2]})
        total_count += count
    
    print(f"\nIngestion Complete. Created {total_count} product-level documents.")
    
    if count > 0:
        print("\nVerifying first 3 results from index...")
        # Since we just updated the index, we can query it
        # Actually, let's just search for 'ice cream' or something general
        result = await engine.query("ice cream")
        print(f"Query Result Meta Count: {len(result.get('metadata', []))}")
        for meta in result.get('metadata', []):
            print(f"- Found: {meta.get('product_name')} | Image: {meta.get('image_url')}")

if __name__ == "__main__":
    # Ensure S3 is enabled for the test if bucket exists
    os.environ["S3_BUCKET_NAME"] = os.getenv("S3_BUCKET_NAME", "supermarket-catalog-images-582604091763")
    asyncio.run(test_ingestion())
