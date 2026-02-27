import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def check_data():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        query = """
            SELECT count(*), string_agg(substring(text FROM 1 FOR 50), '... \n')
            FROM rag.data_supermarket_docs 
            WHERE text ILIKE '%Pepsi%' 
            AND metadata_->>'shop_name' = 'Woolworths';
        """
        
        cur.execute(query)
        count, samples = cur.fetchone()
        
        print(f"Found {count} chunks for 'Pepsi' in Woolworths.")
        if count > 0:
            print(f"Samples:\n{samples}")
            
        # Also check Coles for comparison
        query_coles = """
            SELECT count(*)
            FROM rag.data_supermarket_docs 
            WHERE text ILIKE '%Pepsi%' 
            AND metadata_->>'shop_name' = 'Coles';
        """
        cur.execute(query_coles)
        count_coles = cur.fetchone()[0]
        print(f"Found {count_coles} chunks for 'Pepsi' in Coles.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_data()
