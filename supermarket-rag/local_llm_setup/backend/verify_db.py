import psycopg2
from sqlalchemy import make_url
import os
from dotenv import load_dotenv

load_dotenv()

def check_counts():
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
        
        # Check counts in rag.data_supermarket_docs
        cur.execute("SELECT (metadata_->>'shop_name')::text as shop, COUNT(*) FROM rag.data_supermarket_docs GROUP BY (metadata_->>'shop_name')::text")
        rows = cur.fetchall()
        print("Database Counts (rag.data_supermarket_docs):")
        for row in rows:
            print(f"  {row[0]}: {row[1]}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_counts()
