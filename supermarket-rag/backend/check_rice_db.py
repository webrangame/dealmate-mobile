import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import make_url
import re

def check_rice():
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
    
    # Check for 'rice' as a word
    print("Checking for 'rice' (as a word) in database...")
    # Using Postgres regex for word boundary [[:<:]] and [[:>:]] doesn't work in all versions, 
    # but we can use \m and \M or simpler check.
    # Let's try to fetch more and filter in Python to be sure.
    cur.execute("""
        SELECT metadata_->>'shop_name', metadata_->>'product_name', text 
        FROM rag.data_supermarket_docs 
        WHERE (metadata_->>'product_name' ILIKE '%rice%' OR text ILIKE '%rice%')
        AND (metadata_->>'product_name' NOT ILIKE '%price%' OR metadata_->>'product_name' ILIKE '%rice%')
    """)
    rows = cur.fetchall()
    
    rice_products = []
    for row in rows:
        shop, name, text = row
        # Simple regex to check if "rice" is a word
        if re.search(r'\brice\b', (name or "") + " " + text, re.IGNORECASE):
            rice_products.append(row)
    
    if not rice_products:
        print("No actual rice products found in database.")
    else:
        print(f"Found {len(rice_products)} actual rice products:")
        for row in rice_products[:20]:
            print(f"Store: {row[0]} | Product: {row[1]} | Text snippet: {row[2][:100].replace('\n', ' ')}...")
            
    cur.close()
    conn.close()

if __name__ == "__main__":
    check_rice()
