import asyncio
import os
import logging
from rag_engine import RAGEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    print("=== Local Data Ingestion ===")
    
    # Initialize RAG Engine
    try:
        rag = RAGEngine()
        print("✅ RAG Engine initialized connected to local DB.")
    except Exception as e:
        print(f"❌ Failed to initialize RAG Engine: {e}")
        return

    docs_dir = "/app/documents"
    if not os.path.exists(docs_dir):
        print(f"❌ Documents directory not found: {docs_dir}")
        return

    files = [f for f in os.listdir(docs_dir) if f.endswith(".pdf")]
    if not files:
        print("⚠️ No PDF files found to ingest.")
        return

    print(f"found {len(files)} PDFs: {files}")

    for filename in files:
        print(f"Processing {filename}...")
        try:
            # We use a dummy user_id "local_admin"
            count = await rag.ingest_documents(docs_dir, user_id="local_admin", specific_file=filename)
            print(f"✅ Successfully ingested {count} chunks from {filename}")
        except Exception as e:
            print(f"❌ Error ingesting {filename}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
