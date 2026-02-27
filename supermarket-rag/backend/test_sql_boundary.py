import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import make_url

def test_sql():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    url = make_url(db_url)
    
    conn = psycopg2.connect(
        host=url.host,
        port=url.port,
        database=url.database,
        user=url.username,
        password=url.password,
        sslmode='require'
    )
    cur = conn.cursor()
    
    test_terms = ["rice", "eggs", "Tim Tams"]
    
    for term in test_terms:
        pattern = f"\\m{term}\\M"
        print(f"Testing term: '{term}' with pattern: '{pattern}'")
        cur.execute("""
            SELECT metadata_->>'product_name', count(*) 
            FROM rag.data_supermarket_docs 
            WHERE (metadata_->>'product_name' ~* %s OR text ~* %s)
            GROUP BY 1 LIMIT 5;
        """, (pattern, pattern))
        rows = cur.fetchall()
        print(f"  Found {len(rows)} distinct products (limited to 5).")
        for row in rows:
            print(f"    - {row[0]}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    test_sql()
