import asyncio
import os
import asyncpg
import json

async def test_db_metadata():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not set")
        return
        
    conn = await asyncpg.connect(db_url)
    try:
        query = """
        SELECT id, text, metadata_ 
        FROM rag.data_supermarket_docs 
        WHERE text ILIKE '%ice cream%' 
        LIMIT 20;
        """
        rows = await conn.fetch(query)
        print(f"Found {len(rows)} nodes containing 'ice cream'")
        
        for r in rows:
            meta = json.loads(r['metadata_'])
            print(f"\nNode ID: {r['id']}")
            print(f"Shop: {meta.get('shop_name')}")
            print(f"Product Name: {meta.get('product_name')}")
            print(f"Item Name: {meta.get('item_name')}")
            print(f"Image: {meta.get('page_image_url')}")
            print(f"Text snippet: {r['text'][:100].strip()}...")
            
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(test_db_metadata())
