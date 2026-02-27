import os
import psycopg2
from sqlalchemy import make_url
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def drop_table():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL not set")
        return

    try:
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
        
        table_name = "rag.data_supermarket_docs"
        print(f"Dropping table {table_name}...")
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()
        
        print("Table dropped successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error dropping table: {e}")

if __name__ == "__main__":
    drop_table()
