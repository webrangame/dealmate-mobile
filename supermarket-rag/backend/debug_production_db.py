import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def check_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not found")
        return

    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Check counts in the data_rag_node table if it exists, 
        # but RAG engine uses different table names usually for LlamaIndex
        # LlamaIndex PGVectorStore usually creates a table like 'data_rag'
        
        # Let's list tables first
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'rag'")
        tables = cur.fetchall()
        print(f"Tables in 'rag' schema: {tables}")
        
        for table in tables:
            t_name = table[0]
            print(f"\nAnalyzing table: rag.{t_name}")
            try:
                # Assuming LlamaIndex metadata is in a json column or similar
                # For PGVectorStore, metadata is usually in the 'metadata_' column
                cur.execute(f"SELECT metadata_->>'shop_name' as shop, COUNT(*) FROM rag.{t_name} GROUP BY shop")
                counts = cur.fetchall()
                print(f"Counts per shop: {counts}")
            except Exception as e:
                print(f"Could not query table {t_name}: {e}")
                conn.rollback()

        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

if __name__ == "__main__":
    check_db()
