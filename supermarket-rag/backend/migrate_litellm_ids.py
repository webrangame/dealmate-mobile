import psycopg2
import os
import hashlib
import hmac
from dotenv import load_dotenv
from urllib.parse import urlparse

def make_url(url_str):
    return urlparse(url_str)

def hash_pii(data, salt):
    if not data: return ""
    return hmac.new(
        salt.encode('utf-8'),
        data.lower().strip().encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def migrate_litellm_ids():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    salt = os.getenv("PII_HASH_SALT", "sp8UxnDKXAbQNr1WTcUtq4jiM2DsFSnK3rutoQA5fu0=")
    
    if not db_url:
        print("DATABASE_URL not found")
        return

    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        cur = conn.cursor()
        
        # Fetch all users with their emails (some might be encrypted)
        cur.execute("SELECT id, email, litellm_user_id, email_hash FROM users")
        users = cur.fetchall()
        
        print(f"Migrating LiteLLM IDs for {len(users)} users...")
        
        for user_id, email, current_lite_id, email_hash in users:
            # If we already have email_hash, use it.
            # Otherwise, we might need to decrypt email first (if we have keys), 
            # but ideally we already have email_hash for all users from previous migration.
            
            target_lite_id = email_hash
            
            if not target_lite_id and email:
                 # Fallback hash if email_hash is missing
                 # Note: This assumes email is NOT encrypted or we can't do much here 
                 # without the KMSEncryptor. But migrate_pii.py should have filled email_hash.
                 if "::" not in email:
                     target_lite_id = hash_pii(email, salt)
            
            if target_lite_id and current_lite_id != target_lite_id:
                print(f"Updating User {user_id}: {current_lite_id} -> {target_lite_id}")
                cur.execute(
                    "UPDATE users SET litellm_user_id = %s WHERE id = %s",
                    (target_lite_id, user_id)
                )
        
        conn.commit()
        cur.close()
        conn.close()
        print("Migration complete!")
        
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate_litellm_ids()
