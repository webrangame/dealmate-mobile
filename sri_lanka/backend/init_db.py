import psycopg2
import os
from sqlalchemy import make_url
from dotenv import load_dotenv

load_dotenv()

def init_db():
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/postgres?sslmode=require")
    url = make_url(db_url)
    
    print(f"Connecting to {url.host}...")
    try:
        conn = psycopg2.connect(
            host=url.host,
            port=url.port,
            database=url.database,
            user=url.username,
            password=url.password,
            sslmode='disable'
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Ensuring 'vector' extension exists...")
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        print("Ensuring 'rag' schema exists...")
        cur.execute("CREATE SCHEMA IF NOT EXISTS rag;")
        
        print("Ensuring 'chat_logs' table exists...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rag.chat_logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                query TEXT,
                response TEXT,
                ip_address TEXT,
                metadata JSONB
            );
        """)
        
        print("Database initialization successful!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    init_db()
