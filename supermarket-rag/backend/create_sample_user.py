import os
import psycopg2
from sqlalchemy import make_url
from dotenv import load_dotenv
import datetime

load_dotenv()

def create_user(email="sample_user@niyogen.com", name="Sample User"):
    print(f"==========================================")
    print(f"Creating Sample User in Database")
    print(f"Email: {email}")
    print(f"Name: {name}")
    print(f"==========================================")
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ Error: DATABASE_URL not set in .env")
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
        conn.autocommit = True
        cur = conn.cursor()
        
        # Initialize Encryptor from RAG Engine
        from rag_engine import KMSEncryptor
        kms_key_id = os.getenv("AWS_KMS_KEY_ID")
        encryptor = None
        if kms_key_id:
            encryptor = KMSEncryptor(kms_key_id, os.getenv("AWS_REGION", "us-east-1"))
        
        email_hash = encryptor.hash_pii(email) if encryptor else email
        
        # Check if user already exists
        cur.execute("SELECT id FROM users WHERE email_hash = %s", (email_hash,))
        existing_user = cur.fetchone()
        
        if existing_user:
            print(f"✅ User already exists with ID: {existing_user[0]}")
            return existing_user[0]
            
        # Encrypt PII
        encrypted_email = encryptor.encrypt(email.lower().strip()) if encryptor else email
        encrypted_name = encryptor.encrypt(name.strip()) if encryptor else name

        # Insert sample user
        cur.execute(
            """
            INSERT INTO users (email, email_hash, name, role, is_active, password_hash, created_at, updated_at, pii_version)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
            RETURNING id;
            """,
            (encrypted_email, email_hash, encrypted_name, "user", True, "dummy_hash_for_testing", datetime.datetime.now(), datetime.datetime.now())
        )
        
        user_id = cur.fetchone()[0]
        print(f"✅ Success! Created User ID: {user_id}")
        
        cur.close()
        conn.close()
        return user_id
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return None

if __name__ == "__main__":
    create_user()
