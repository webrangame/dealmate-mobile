import os
import psycopg2
import hmac
import hashlib
from sqlalchemy import make_url
from dotenv import load_dotenv
from rag_engine import KMSEncryptor

load_dotenv()

def verify_encrypted_login(email="rangap@niyogen.com"):
    print(f"--- Verifying Encrypted Login for {email} ---")
    
    db_url = os.getenv("DATABASE_URL")
    kms_key_id = os.getenv("AWS_KMS_KEY_ID")
    salt = os.getenv("PII_HASH_SALT", "default-salt-change-me")
    
    encryptor = KMSEncryptor(kms_key_id, os.getenv("AWS_REGION", "us-east-1"))
    
    # 1. Calculate Hash (this is what the backend/market_place would do)
    email_hash = hmac.new(
        salt.encode('utf-8'),
        email.lower().strip().encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"Calculated Hash: {email_hash}")
    
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
        
        # 2. Lookup by hash
        cur.execute("SELECT email, name FROM users WHERE email_hash = %s", (email_hash,))
        row = cur.fetchone()
        
        if not row:
            print("❌ Error: User not found via hash")
            return

        encrypted_email, encrypted_name = row
        print(f"Fetch Result (Encrypted):")
        print(f"  Email: {encrypted_email[:50]}...")
        print(f"  Name: {encrypted_name[:50]}...")
        
        # 3. Decrypt
        decrypted_email = encryptor.decrypt(encrypted_email)
        decrypted_name = encryptor.decrypt(encrypted_name)
        
        print(f"Decrypted Result:")
        print(f"  Email: {decrypted_email}")
        print(f"  Name: {decrypted_name}")
        
        if decrypted_email.lower().strip() == email.lower().strip():
            print("✅ SUCCESS: Decrypted email matches original!")
        else:
            print("❌ FAILURE: Decrypted email mismatch!")
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Verification Failed: {e}")

if __name__ == "__main__":
    verify_encrypted_login()
