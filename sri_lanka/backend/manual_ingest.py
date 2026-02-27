import os
import shutil
import asyncio
from dotenv import load_dotenv

# Load env before importing rag_engine which instantiates RAGEngine
load_dotenv() 

from rag_engine import rag_engine

async def main():
    upload_dir = "uploaded_docs"

    if not os.path.exists(upload_dir):
        print(f"Directory {upload_dir} not found.")
        return

    print("Starting ingestion from uploaded_docs...")
    try:
        # We ingest the entire directory as per RAGEngine.ingest_documents
        count = await rag_engine.ingest_documents(upload_dir)
        print(f"Successfully ingested {count} documents.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    asyncio.run(main())
