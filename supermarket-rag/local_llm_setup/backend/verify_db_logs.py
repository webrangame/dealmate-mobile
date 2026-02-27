import os
import psycopg2
import json

db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("DATABASE_URL not found")
    exit(1)

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Check if table exists
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'rag' AND table_name = 'chat_logs')")
    exists = cur.fetchone()[0]
    print(f"Table rag.chat_logs exists: {exists}")
    
    if exists:
        # Get last 5 logs
        cur.execute("SELECT id, timestamp, query, user_id FROM rag.chat_logs ORDER BY timestamp DESC LIMIT 5")
        rows = cur.fetchall()
        print("\nLast 5 Chat Logs:")
        for row in rows:
            print(f"ID: {row[0]} | Time: {row[1]} | User: {row[3]} | Query: {row[2]}")
            
        # Count logs from today
        cur.execute("SELECT COUNT(*) FROM rag.chat_logs WHERE timestamp > CURRENT_DATE")
        count = cur.fetchone()[0]
        print(f"\nTotal logs today: {count}")
        
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
