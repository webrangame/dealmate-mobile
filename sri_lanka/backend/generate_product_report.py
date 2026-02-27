import os
import psycopg2
import csv
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def generate_report():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("Fetching all data from database...")
        
        # Get all text chunks with shop name
        cur.execute("""
            SELECT 
                metadata_->>'shop_name' as shop, 
                metadata_->>'page' as page, 
                text 
            FROM rag.data_supermarket_docs 
            ORDER BY metadata_->>'shop_name', (metadata_->>'page')::int;
        """)
        
        rows = cur.fetchall()
        
        filename = "full_product_list.csv"
        print(f"Writing {len(rows)} records to {filename}...")
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Shop", "Page", "Content"])
            
            for shop, page, text in rows:
                # Clean text slightly
                clean_text = text.replace("\n", " ").strip()
                writer.writerow([shop, page, clean_text])
                
        print(f"Successfully generated {filename} with {len(rows)} rows.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_report()
