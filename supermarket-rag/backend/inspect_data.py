import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def inspect_data():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("=== COLES SAMPLES ===")
        cur.execute("SELECT text FROM rag.data_supermarket_docs WHERE metadata_->>'shop_name' = 'Coles' LIMIT 5")
        for row in cur.fetchall():
            print(f">>> {row[0][:200]}\n")
        
        print("\n=== WOOLWORTHS SAMPLES ===")
        cur.execute("SELECT text FROM rag.data_supermarket_docs WHERE metadata_->>'shop_name' = 'Woolworths' LIMIT 5")
        for row in cur.fetchall():
            print(f">>> {row[0][:200]}\n")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_data()
