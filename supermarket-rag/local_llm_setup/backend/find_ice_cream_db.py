import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def find_ice_cream():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not found")
        return

    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Search for text containing 'ice cream'
        cur.execute("""
            SELECT metadata_->>'shop_name' as shop, text, metadata_->>'page' as page
            FROM rag.data_supermarket_docs 
            WHERE text ILIKE '%ice cream%'
        """)
        results = cur.fetchall()
        print(f"Found {len(results)} nodes containing 'ice cream'")
        
        for r in results:
            print(f"\nShop: {r[0]}, Page: {r[2]}")
            print(f"Content: {r[1][:200]}...")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

if __name__ == "__main__":
    find_ice_cream()
