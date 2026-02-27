import os
import psycopg2
import json
from sqlalchemy import make_url
from dotenv import load_dotenv

load_dotenv()

def find_url():
    target_url = "https://supermarket-catalog-images-582604091763.s3.us-east-1.amazonaws.com/catalog-pages/Coles/Coles_page_3_1771056128.jpg"
    print(f"Searching for metadata containing URL: {target_url}")
    
    db_url = os.getenv("DATABASE_URL")
    url = make_url(db_url)
    try:
        conn = psycopg2.connect(
            host=url.host,
            port=url.port,
            database=url.database,
            user=url.username,
            password=url.password,
            sslmode='require'
        )
        cur = conn.cursor()
        
        cur.execute("""
            SELECT node_id, text, metadata_ 
            FROM rag.data_supermarket_docs 
            WHERE metadata_->>'page_image_url' = %s
        """, (target_url,))
        
        rows = cur.fetchall()
        print(f"Found {len(rows)} matching nodes.")
        
        for r in rows:
            print(f"\nNode ID: {r[0]}")
            print(f"Text: {r[1][:200]}...")
            print(f"Metadata: {json.dumps(r[2], indent=2)}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_url()
