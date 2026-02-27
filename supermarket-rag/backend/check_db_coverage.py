import psycopg2
import json

DATABASE_URL = "postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/postgres?sslmode=require"

FAILED_PRODUCTS = [
    "Coca-Cola",
    "Strawberries",
    "Annalisa Tomatoes",
    "Eggs",
    "Chicken Breast",
    "Bananas",
    "Toilet Paper",
    "Rice",
    "Dine Wet Cat Food",
    "Purina One",
    "Fancy Feast",
    "Temptations",
    "Supercoat",
    "Pedigree",
    "Pepsi Max"
]

def check_coverage():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print(f"{'Product Search':<25} | {'Count':<5} | {'Matches Found'}")
        print("-" * 60)
        
        for prod in FAILED_PRODUCTS:
            # Query metadata JSONB directly for better precision
            query = "SELECT COUNT(*) FROM rag.data_supermarket_docs WHERE is_enabled = TRUE AND (text ILIKE %s OR metadata_->>'product_name' ILIKE %s)"
            cur.execute(query, (f"%{prod}%", f"%{prod}%"))
            count = cur.fetchone()[0]
            
            # Get some example matches
            cur.execute("SELECT metadata_->>'product_name' FROM rag.data_supermarket_docs WHERE is_enabled = TRUE AND (text ILIKE %s OR metadata_->>'product_name' ILIKE %s) LIMIT 3", (f"%{prod}%", f"%{prod}%"))
            examples = [r[0] for r in cur.fetchall() if r[0]]
            example_str = ", ".join(examples[:3])
            
            print(f"{prod:<25} | {count:<5} | {example_str}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_coverage()
