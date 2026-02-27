import os
import sys
from rag_engine import rag_engine

def decrypt_logs(ids):
    for log_id in ids:
        try:
            from sqlalchemy import make_url
            import psycopg2
            url = make_url(rag_engine.db_url)
            conn = psycopg2.connect(
                host=url.host,
                port=url.port,
                database=url.database,
                user=url.username,
                password=url.password,
                sslmode='require'
            )
            cur = conn.cursor()
            cur.execute("SELECT query FROM rag.chat_logs WHERE id = %s", (log_id,))
            row = cur.fetchone()
            if row:
                encrypted_query = row[0]
                decrypted = rag_engine.encryptor.decrypt(encrypted_query)
                print(f"Log ID {log_id}: {decrypted}")
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error decrypting log {log_id}: {e}")

if __name__ == "__main__":
    decrypt_logs([1576, 1577])
